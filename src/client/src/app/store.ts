import {configureStore} from "@reduxjs/toolkit";
import {rootReducer} from "./types.ts";
import {apiMiddleware} from "./middleware/apiMiddleware.ts";
import {socketIOMiddleware} from "./middleware/socketIOMiddleware.ts";

export const store = configureStore({
    reducer: rootReducer,
    middleware: getDefaultMiddleware => getDefaultMiddleware()
        .concat(apiMiddleware)
        .concat(socketIOMiddleware)
});
