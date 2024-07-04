// src/components/CandidateLayout.jsx
import React from 'react';
import { Layout } from 'antd';
import { Outlet } from 'react-router-dom';
import CandidateNavbar from '../Layouts/CandidateNavBar';

const { Header, Content } = Layout;

function CandidateLayout() {
    return (
        <Layout>
            <Header>
                <CandidateNavbar />
            </Header>
            <Content style={{ padding: '50px' }}>
                <Outlet /> {/* This will render the nested routes */}
            </Content>
        </Layout>
    );
}

export default CandidateLayout;
