import { configureStore } from "@reduxjs/toolkit";
import rootReducer from "./rootReducer";
import loggerMiddleware from "./middleware/logger";

const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMidlleware) => getDefaultMidlleware().concat(loggerMiddleware)
});

export type AppDispatch = typeof store.dispatch;
export type RoorState = ReturnType<typeof store.getState>;
export default store;