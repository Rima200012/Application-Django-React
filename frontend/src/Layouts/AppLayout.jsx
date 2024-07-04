import React from "react";
import { Layout } from "antd";
import CandidateSidebar from "./CandidateSidebar";
import RecruiterSidebar from "./RecruiterSidebar";
import Navbar from "../Navbar";  // Assuming you still need the Navbar

const AppLayout = () => {
    const userType = localStorage.getItem('Role'); // 'candidate' or 'recruiter'

    return (
        <Layout style={{ minHeight: "100vh" }}>
            {userType === 'candidate' ? <CandidateSidebar /> : <RecruiterSidebar />}
            <Layout>
                <Navbar />  {/* Add Navbar if it's required */}
                <Layout.Content style={{ margin: "24px 16px 0" }}>
                    <div style={{ padding: 24, background: "#fff", minHeight: 360 }}>
                        <Container />
                    </div>
                </Layout.Content>
            </Layout>
        </Layout>
    );
};

export default AppLayout;
