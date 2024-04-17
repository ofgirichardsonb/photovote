import React from "react";
import {useAppSelector} from "../../app/types.ts";

const Home : React.FC = () => {
    const displayName = useAppSelector(state => state.auth.displayName)
    const socketId = useAppSelector(state => state.socketio.socketId)

    return (
        <>
            <div className="content">
                <p>
                    Hello, {displayName ?? "world"}!
                </p>
                <p>
                    WebSocket ID: <b>{socketId ?? "Not connected"}</b>
                </p>
            </div>
        </>
    )
}

export {Home}