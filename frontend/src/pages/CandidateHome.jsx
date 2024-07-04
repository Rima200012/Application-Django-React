import React from 'react';
import CandidateNavbar from '../Layouts/CandidateNavBar';
import { Layout, Typography } from 'antd';
import '../styles/candidatehome.css';

const { Header, Content } = Layout;
const { Title, Paragraph } = Typography;

function CandidateHomePage() {
    return (
        <Layout>
            
            <Content style={{ padding: '50px' }}>
                <div className="container" style={{ background: '#fff', padding: '24px', minHeight: '280px' }}>
                    <Title>Welcome to Django Jobs</Title>
                    <Paragraph>Candidate Dashboard</Paragraph>
                    {/* The PowerBI integration or other dashboard content will go here */}
                </div>
            </Content>
        </Layout>
    );
}

export default CandidateHomePage;