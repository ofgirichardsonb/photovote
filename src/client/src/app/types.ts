import {Action, combineReducers, ThunkDispatch} from "@reduxjs/toolkit";
import authReducer from "../features/auth/authSlice.ts"
import socketIOReducer from "../features/socketio/socketIOslice.ts";
import {TypedUseSelectorHook, useDispatch, useSelector} from "react-redux";

export const rootReducer = combineReducers({
    auth: authReducer,
    socketio: socketIOReducer
});

export type RootState = ReturnType<typeof rootReducer>
export type AppDispatch = ThunkDispatch<RootState, unknown, Action>

export const useAppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;