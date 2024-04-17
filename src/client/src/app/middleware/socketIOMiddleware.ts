import {Middleware} from "@reduxjs/toolkit";
import {AppDispatch, RootState} from "../types.ts";
import {io} from "socket.io-client";
import {responseReceived, socketConnected} from "../../features/socketio/socketIOslice.ts";

export type SOCKETIO_CONNECT = 'SOCKETIO_CONNECT'


export const socketIOMiddleware: Middleware<{}, RootState, AppDispatch> = storeAPI => next => action => {
    if (action && typeof action === 'object' && 'type' in action) {
        if (action.type == 'SOCKETIO_CONNECT') {
            const wsUrl = import.meta.env.VITE_WS_URL;
            const socket = io(wsUrl, {
                path: "/socket.io/",
                transports: ["websocket", "polling"],
                closeOnBeforeunload: true
            })
            socket.on("connect", () => {
                console.log(`Connected with id ${socket.id}`)
                storeAPI.dispatch(socketConnected(socket.id ?? null))
            })
            socket.on("connect_error", err => console.error(err.message))
            socket.on("disconnect", (reason, description) => {
                storeAPI.dispatch(socketConnected(null))
                console.log(`Disconnected: ${reason} (${description})`)
            })
            socket.on("response", (response) => {
                const decoded = new TextDecoder("utf-8").decode(response)
                console.log(`Response received: ${decoded}`)
                const obj = JSON.parse(decoded)
                if ('request_id' in obj) {
                    const state = storeAPI.getState()
                    const requestMap = state.socketio.requestMap
                    const action = requestMap[obj.request_id]
                    if (action) {
                        storeAPI.dispatch(responseReceived(obj.request_id))
                        storeAPI.dispatch({type: action, payload: obj.data})
                    }
                }
            });
        }
        // we don't skip reducers here, it's enough to initiate the connection.
    }
    return next(action);
}