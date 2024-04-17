import React, {useEffect} from "react";
import {useAppDispatch} from "../../app/types.ts";
import { codeReceived } from "../../features/auth/authSlice.ts";
import {useNavigate} from "react-router-dom";

const LoginCallback: React.FC = () => {
    const dispatch = useAppDispatch()
    const navigate = useNavigate()

    useEffect(() => {
        if (location.search) {
            const code = new URLSearchParams(location.search).get('code')
            if (code) {
                dispatch(codeReceived({code}))
                navigate("/", {
                    relative: "route",
                    replace: true
                })
            }
        }
    }, [location.search]);

    return <div></div>
}

export {LoginCallback}