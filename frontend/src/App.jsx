import React, { useState } from "react";
import { Route, Routes, Navigate, useNavigate, useLocation } from "react-router-dom";
import { Menu, Layout, Button } from "antd";
import {
  HomeOutlined, SearchOutlined, ProfileOutlined, PoweroffOutlined, PlusOutlined,
  EditOutlined, FileTextOutlined, MenuFoldOutlined, MenuUnfoldOutlined
} from "@ant-design/icons";
import Login from "./pages/login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import RecruiterHomePage from './pages/RecruiterHome';
import CandidateHomePage from './pages/CandidateHome';
import AddJobPost from './pages/AddJobPost';
import ManageJobPosts from './pages/ManageJobPosts';
import JobApplications from "./pages/JobApplications";
import UpdateJobPost from "./pages/UpdateJobPost";
import ManageProfile from './pages/ManageProfile';
import MyApplications from "./pages/MyApplications";
import SearchJobs from "./pages/SearchJobs";
import ApplyJob from "./pages/ApplyJob";
import ProtectedRoute from "./components/ProtectedRoute";
import CandidateLayout from "./components/CandidateLayout";
import RecruiterLayout from "./components/RecruiterLayout";
import EmailVerification from './components/EmailVerification';

import Auth from "./Auth";
import Callback from "./callback";
import { AuthProvider } from "./context/AuthContext";
import 'antd/dist/reset.css';
import "./App.css";

const { Sider, Content } = Layout;

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function SideMenu({ collapsed }) {
  const navigate = useNavigate();
  const role = localStorage.getItem('role'); // Assuming role is stored in localStorage

  const candidateMenuItems = [
    { label: "Home", key: "/candidate-home", icon: <HomeOutlined /> },
    { label: "Search Jobs", key: "/candidate-home/search-jobs", icon: <SearchOutlined /> },
    { label: "My Applications", key: "/candidate-home/my-applications", icon: <FileTextOutlined /> },
    { label: "Manage Profile", key: "/candidate-home/manage-profile", icon: <ProfileOutlined /> },
  ];

  const recruiterMenuItems = [
    { label: "Home", key: "/recruiter-home", icon: <HomeOutlined /> },
    { label: "Add Job Post", key: "/recruiter-home/add-job-post", icon: <PlusOutlined /> },
    { label: "Manage Job Posts", key: "/recruiter-home/manage-job-posts", icon: <EditOutlined /> },
    { label: "Manage Profile", key: "/recruiter-home/manage-profile", icon: <ProfileOutlined /> },
  ];

  const menuItems = role === 'recruiter' ? recruiterMenuItems : candidateMenuItems;

  return (
    <Sider width={240} collapsible collapsed={collapsed} trigger={null} style={{ height: '100vh', backgroundColor: '#ffffff', color: '#000000', borderRight: '1px solid #e8e8e8' }}>
      <div className="logo" />
      <Menu
        mode="inline"
        theme="light"
        style={{ height: '100%', borderRight: 0 }}
        onClick={({ key }) => {
          if (key === "/logout") {
            localStorage.clear();
            navigate('/login');
          } else {
            navigate(key);
          }
        }}
        defaultSelectedKeys={[window.location.pathname]}
        items={menuItems}
      />
      <Menu
        mode="inline"
        theme="light"
        style={{ position: 'absolute', bottom: 0, width: '100%' }}
        items={[
          {
            key: '/logout',
            icon: <PoweroffOutlined />,
            label: 'Log out',
            danger: true
          },
        ]}
        onClick={({ key }) => {
          if (key === '/logout') {
            localStorage.clear();
            navigate('/login');
          }
        }}
      />
    </Sider>
  );
}

function App() {
  const location = useLocation();
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register';
  const [collapsed, setCollapsed] = useState(false);

  return (
    <AuthProvider>
      <Layout className={`app-container ${!isAuthPage ? 'background-image' : ''}`} style={{ height: '100vh' }}>
        {!isAuthPage && (
          <>
            <SideMenu collapsed={collapsed} />
            <Button className="toggle-button" type="primary" onClick={() => setCollapsed(!collapsed)} style={{ margin: '16px' }}>
              {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            </Button>
          </>
        )}
        <Layout style={{ marginLeft: isAuthPage ? 0 : collapsed ? 80 : 240, height: '100vh', overflow: 'hidden' }}>
          <Content style={{ padding: isAuthPage ? '0' : '24px', height: '100%', overflowY: isAuthPage ? 'hidden' : 'auto' }}>
            <Routes>
              <Route path="/auth" element={<Auth />} />
              <Route path="/auth/callback" element={<Callback />} />
              <Route path="/" element={<Navigate to="/login" />} />
              <Route path="/login" element={<Login />} />
              <Route path="/logout" element={<Logout />} />
              <Route path="/register" element={<RegisterAndLogout />} />
              <Route path="/verify_email/:uid/:token" element={<EmailVerification />} />
              <Route path="*" element={<NotFound />} />
              <Route
                path="/candidate-home"
                element={
                  <ProtectedRoute role="candidate">
                    <CandidateLayout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<CandidateHomePage />} />
                <Route path="search-jobs" element={<SearchJobs />} />
                <Route path="my-applications" element={<MyApplications />} />
                <Route path="jobposts/:jobId/apply" element={<ApplyJob />} />
                <Route path="manage-profile" element={<ManageProfile />} />
              </Route>
              <Route
                path="/recruiter-home"
                element={
                  <ProtectedRoute role="recruiter">
                    <RecruiterLayout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<RecruiterHomePage />} />
                <Route path="add-job-post" element={<AddJobPost />} />
                <Route path="manage-job-posts" element={<ManageJobPosts />} />
                <Route path="jobposts/:jobId/applicants" element={<JobApplications />} />
                <Route path="jobposts/:jobId/applicants/status" element={<JobApplications />} />
                <Route path="jobposts/:jobId/update" element={<UpdateJobPost />} />
                <Route path="manage-profile" element={<ManageProfile />} />
              </Route>
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </AuthProvider>
  );
}

export default App;
