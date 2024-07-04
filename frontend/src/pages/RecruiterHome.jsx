import React from 'react';
import RecruiterNavbar from '../Layouts/RecruiterNavbar';
import { Layout, Typography } from 'antd';
import '../styles/RecruiterHome.css';

const { Header, Content } = Layout;
const { Title, Paragraph } = Typography;

function RecruiterHomePage() {
    return (
        <Layout>
            
            <Content style={{ padding: '50px' }}>
                <div className="container" style={{ background: '#fff', padding: '24px', minHeight: '280px' }}>
                    <Title>Welcome to Django Jobs</Title>
                    <Paragraph>Recruiter Dashboard</Paragraph>
                    {/* The PowerBI integration or other dashboard content will go here */}
                </div>
            </Content>
        </Layout>
    );
}

export default RecruiterHomePage;
