import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
 // Change to named import
import api from "../api";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants";
import { useState, useEffect } from "react";

function ProtectedRoute({ children, role }) {
    const [isAuthorized, setIsAuthorized] = useState(null);
    const [userRole, setUserRole] = useState(null);

    useEffect(() => {
        auth().catch(() => setIsAuthorized(false));
    }, []);

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            const res = await api.post("/users/token/refresh/", { refresh: refreshToken });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthorized(true);
                await fetchUserRole(res.data.access);
            } else {
                setIsAuthorized(false);
            }
        } catch (error) {
            console.log(error);
            setIsAuthorized(false);
        }
    };

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setIsAuthorized(false);
            return;
        }
        const decoded = jwtDecode(token);
        console.log(decoded);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        if (tokenExpiration < now) {
            await refreshToken();
        } else {
            setIsAuthorized(true);
            await fetchUserRole(token);
        }
    };

    const fetchUserRole = async (token) => {
        try {
            const res = await api.get("/users/get_user_role/", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setUserRole(res.data.role);
            localStorage.setItem("role", res.data.role);
        } catch (error) {
            console.log(error);
            setIsAuthorized(false);
        }
    };

    if (isAuthorized === null || userRole === null) {
        return <div>Loading...</div>;
    }

    if (isAuthorized && role && userRole !== role) {
        return <Navigate to="/not-authorized" />;
    }

    return isAuthorized ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;
