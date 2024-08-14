import React from 'react';
import { Layout } from 'antd';
import PowerBIEmbedComponent from '../components/PowerBIEmbedComponent';
import '../styles/RecruiterHome.css';

const { Content } = Layout;

function RecruiterHomePage() {
    return (
        <Layout className="recruiter-home-page">
            <Content>
                <div className="recruiter-dashboard-container">
                    <div className="recruiter-dashboard-embed">
                        <PowerBIEmbedComponent userType="recruiter" />
                    </div>
                </div>
            </Content>
        </Layout>
    );
}

export default RecruiterHomePage;
