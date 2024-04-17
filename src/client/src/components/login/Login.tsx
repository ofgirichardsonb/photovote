import {Button} from "@mui/material";
import {useAppDispatch, useAppSelector} from "../../app/types.ts";
import {loggedOut, loginInitiated} from "../../features/auth/authSlice.ts";
import React, {useEffect} from "react";

const Login: React.FC = () => {
    const loginInitiatedAction = {
        type: 'API_ACTION',
        payload: {
            uri: "/security/login-initiated",
            method: "POST",
            responseAction: "auth/authUrlReceived",
            data: {
                callback_uri: `${import.meta.env.VITE_BASE_URL}/callback`,
            }
        }
    }

    const codeReceivedAction = (code: string) => {
        return {
            type: 'API_ACTION',
            payload: {
                uri: `/security/code-received`,
                method: "POST",
                responseAction: 'auth/tokenReceived',
                data: {
                    code,
                    callback_uri: `${import.meta.env.VITE_BASE_URL}/callback`,
                }
            }
        }
    }

    const tokenReceivedAction = {
        type: 'API_ACTION',
        payload: {
            uri: `/security/token-received`,
            method: "GET",
            responseAction: "auth/userInfoReceived",
            data: null
        }
    };

    const status = useAppSelector(state => state.auth.status)
    const authUrl = useAppSelector(state => state.auth.authUrl)
    const code = useAppSelector(state => state.auth.code)
    const accessToken = useAppSelector(state => state.auth.accessToken)
    const socketId = useAppSelector(state => state.socketio.socketId)
    const loginName = useAppSelector(state => state.auth.loginName)
    const displayName = useAppSelector(state => state.auth.displayName)
    const loggedIn = useAppSelector(state => state.auth.status === 'loggedIn')
    const dispatch = useAppDispatch()

    useEffect(() => {
        console.log(`Auth status changed to '${status}'`)
        if (status === 'loginInitiated')
            dispatch(loginInitiatedAction)
    }, [status, dispatch])

    useEffect(() => {
        console.log(`Auth URL changed to '${authUrl}'`)
        if (authUrl)
            window.open(authUrl, "_self")
    }, [authUrl, dispatch])

    useEffect(() => {
        // the socket will have to reconnect upon receiving the code, so wait for it
        if (code && socketId) {
            console.log(`Code changed to '${code}'`)
            dispatch(codeReceivedAction(code))
        }
    }, [code, dispatch, socketId])

    useEffect(() => {
        console.log(`Access token changed to ${accessToken}`)
        if (accessToken)
            dispatch(tokenReceivedAction)
    }, [accessToken])

    useEffect(() => {
        console.log(`Login name changed to ${loginName}`)
    }, [loginName])

    useEffect(() => {
        console.log(`Display name changed to ${displayName}`)
    }, [displayName])

    return loggedIn ?
        (
            <div>
                <p>Logged in as <b>{loginName}</b></p>
                <Button onClick={() => dispatch(loggedOut())}>Logout</Button>
            </div>
        )
        :
        (
            <div><Button onClick={() => { dispatch(loginInitiated()) }}>Login</Button></div>
        )
}

export {Login}