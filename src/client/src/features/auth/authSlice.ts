import {createSlice, PayloadAction} from "@reduxjs/toolkit";

interface AuthState {
    authUrl: string | null
    code: string | null
    accessToken: string | null
    refreshToken: string | null
    loginName: string | null
    displayName: string | null
    status: string
};

const initialState: AuthState = {
    authUrl: null,
    code: null,
    accessToken: null,
    refreshToken: null,
    loginName: null,
    displayName:  null,
    status: 'loggedOut'
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        loginInitiated: (state) => {
            state.status = 'loginInitiated'
        },
        authUrlReceived: (state, action: PayloadAction<{authUrl: string}>) => {
            state.authUrl = action.payload.authUrl
            state.status = 'loggingIn'
        },
        codeReceived: (state, action: PayloadAction<{code: string}>) => {
            state.authUrl = null
            state.code = action.payload.code
            state.status = 'authorizing'
        },
        tokenReceived: (state, action: PayloadAction<{accessToken: string, refreshToken: string}>) => {
            state.code = null
            state.accessToken = action.payload.accessToken
            state.refreshToken = action.payload.refreshToken
            state.status = 'loadingProfile'
        },
        userInfoReceived: (state, action: PayloadAction<{loginName: string, displayName: string}>) => {
            state.loginName = action.payload.loginName
            state.displayName = action.payload.displayName
            state.status = 'loggedIn'
        },
        loggedOut: (state) => {
            state.authUrl = null
            state.code = null
            state.accessToken = null
            state.refreshToken = null
            state.loginName = null
            state.displayName = null
            state.status = 'loggedOut'
        }
    },
    extraReducers: (_) => {
    }
});

export const {
    loginInitiated,
    authUrlReceived,
    codeReceived,
    tokenReceived,
    userInfoReceived,
    loggedOut
} = authSlice.actions

export default authSlice.reducer
