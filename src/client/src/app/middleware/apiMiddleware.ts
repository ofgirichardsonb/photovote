import {Middleware} from "@reduxjs/toolkit";
import {AppDispatch, RootState} from "../types.ts";
import {doApiRequest} from "../../features/socketio/socketIOslice.ts";

export type API_ACTION = 'API_ACTION'
export type HttpMethod = 'GET' | 'PUT' | 'POST' | 'PATCH' | 'DELETE'

export interface IApiAction {
    type: API_ACTION
    payload: {
        uri: string
        method: HttpMethod
        headers?: any,
        data?: any,
        responseAction?: string | null
    }
}

export const apiMiddleware: Middleware<{}, RootState, AppDispatch> = storeAPI => next => action => {
    if (action && typeof action === 'object' && 'type' in action) {
        if (action.type === 'API_ACTION') {
            let apiAction = action as IApiAction
            storeAPI.dispatch(doApiRequest({action: apiAction}))
            return;
        }
    }
    return next(action);
}
