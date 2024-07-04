import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, Button } from 'antd';

function RecruiterNavbar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <Menu mode="horizontal" theme="dark">
            <Menu.Item key="home">
        <Link to="/recruiter-home">Home</Link>
      </Menu.Item>
      <Menu.Item key="add-job-post">
        <Link to="/recruiter-home/add-job-post">Add Job Post</Link>
      </Menu.Item>
      <Menu.Item key="manage-job-posts">
        <Link to="/recruiter-home/manage-job-posts">Manage Job Posts</Link>
      </Menu.Item>
            <Menu.Item key="manage-profile">
                <Link to="/recruiter-home/manage-profile">Manage Profile</Link>
            </Menu.Item>
            <Menu.Item key="logout" style={{ marginLeft: 'auto' }}>
                <Button type="primary" danger onClick={handleLogout}>
                    Logout
                </Button>
            </Menu.Item>
        </Menu>
    );
}

export default RecruiterNavbar;