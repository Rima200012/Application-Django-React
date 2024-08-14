import React from 'react';
import { Layout } from 'antd';
import PowerBIEmbedComponent from '../components/PowerBIEmbedComponent';
import '../styles/candidatehome.css';

const { Content } = Layout;

function CandidateHomePage() {
    return (
        <Layout className="candidate-home-page">
            <Content>
                <div className="candidate-dashboard-container">
                    <div className="candidate-dashboard-embed">
                        <PowerBIEmbedComponent userType="candidate" />
                    </div>
                </div>
            </Content>
        </Layout>
    );
}

export default CandidateHomePage;
