import React from 'react';
import { Layout } from 'antd';
import { Outlet } from 'react-router-dom';

const { Header, Content } = Layout;

function RecruiterLayout() {
    return (
        <Layout>
            <Header>
                {/* Header content if needed */}
            </Header>
            <Content style={{ padding: '50px' }}>
                <Outlet /> {/* This will render the nested routes */}
            </Content>
        </Layout>
    );
}

export default RecruiterLayout;