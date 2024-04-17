import './App.css'
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Home} from "./components/home/Home.tsx";
import {LoginCallback} from "./components/login/LoginCallback.tsx";
import {Login} from "./components/login/Login.tsx";
import React, {useEffect} from "react";
import {useAppDispatch} from "./app/types.ts";

const App: React.FC = () => {
    const dispatch = useAppDispatch()

    useEffect(() => {
        dispatch({type: 'SOCKETIO_CONNECT'})
    }, [dispatch]);

    return (
        <>
        <div className="row"><Login/></div>
        <BrowserRouter>
            <div>
                <Routes>
                    <Route element={<LoginCallback />} path="/callback" />
                    <Route element={<Home />} path="/" />
                </Routes>
            </div>
        </BrowserRouter>
        </>
    );
}

export default App
