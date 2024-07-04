// src/components/RecruiterLayout.jsx
import React from 'react';
import { Layout } from 'antd';
import { Outlet } from 'react-router-dom';
import RecruiterNavbar from '../Layouts/RecruiterNavbar';

const { Header, Content } = Layout;

function RecruiterLayout() {
    return (
        <Layout>
            <Header>
                <RecruiterNavbar />
            </Header>
            <Content style={{ padding: '50px' }}>
                <Outlet /> {/* This will render the nested routes */}
            </Content>
        </Layout>
    );
}

export default RecruiterLayout;
