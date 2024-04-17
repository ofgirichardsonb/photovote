import {createAsyncThunk, createSlice, PayloadAction} from "@reduxjs/toolkit";
import {IApiAction} from "../../app/middleware/apiMiddleware.ts";
import {RootState} from "../../app/types.ts";
import {v4 as uuidv4} from "uuid";

export interface SocketIOState {
    socketId: string | null
    requestMap: Record<string, string>
}

const initialState: SocketIOState = {
    socketId: null,
    requestMap: {},
}

export const doApiRequest = createAsyncThunk<
    void,
    {action: IApiAction},
    {state: RootState, rejectValue: {message: string}}
>(
    'socketIO/doApiRequest',
    async ({action}, {dispatch, getState, rejectWithValue}) => {
        try {
            const state = getState()
            const requestId = uuidv4()
            if (action.payload.responseAction)
                dispatch(requestSent({requestId, reducerType: action.payload.responseAction}))
            let payload = {}
            if (action.payload.data)
                payload = {...action.payload.data}
            payload = {
                ...payload,
                request_id: requestId,
                reply_to: state.socketio.socketId,
                scope: 'openid'
            }
            let headers = {}
            if (action.payload.headers)
                headers = {...action.payload.headers}
            headers = {
                ...headers,
                'Content-Type': 'application/json',
            }
            if (state.auth.accessToken)
                headers = {
                    ...headers,
                    'Authorization': `Bearer ${state.auth.accessToken}`
                }
            let q = ''
            if (action.payload.method === 'GET' || action.payload.method === 'DELETE' && action.payload.data)
                q = '?' + new URLSearchParams(payload).toString()
            await fetch(`${import.meta.env.VITE_API_BASE_URL}${action.payload.uri}${q}`, {
                method: action.payload.method,
                // do not send a body with GET or DELETE requests
                body: action.payload.method === 'GET' || action.payload.method === 'DELETE'
                    ? null
                    : JSON.stringify(payload),
                headers: headers
            });
        }
        catch (error: any) {
            return rejectWithValue(error.message)
        }
    }
)

const socketIOslice = createSlice({
    name: 'socketIO',
    initialState,
    reducers: {
        requestSent: (state, action: PayloadAction<{requestId: string, reducerType: string}>) => {
            state.requestMap[action.payload.requestId] = action.payload.reducerType
        },
        responseReceived: (state, action: PayloadAction<string>) => {
            delete state.requestMap[action.payload]
        },
        socketConnected: (state, action: PayloadAction<string | null>) => {
            state.socketId = action.payload
        },
    },
    extraReducers: _ => {}
});

export const {
    requestSent,
    responseReceived,
    socketConnected
} = socketIOslice.actions;

export default socketIOslice.reducer