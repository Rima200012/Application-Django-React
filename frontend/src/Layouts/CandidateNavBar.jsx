import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, Button } from 'antd';

function CandidateNavbar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <Menu mode="horizontal" theme="dark">
            <Menu.Item key="home">
        <Link to="/candidate-home">Home</Link>
      </Menu.Item>
      <Menu.Item key="search-jobs">
        <Link to="/candidate-home/search-jobs">Search Jobs</Link>
        
      </Menu.Item>
      
      
      <Menu.Item key="my-applications">
        <Link to="/candidate-home/my-applications">My Applications</Link>
      </Menu.Item>
      <Menu.Item key="manage-profile">
        <Link to="/candidate-home/manage-profile">Manage Profile</Link>
      </Menu.Item>
           
            <Menu.Item key="logout" style={{ marginLeft: 'auto' }}>
                <Button type="primary" danger onClick={handleLogout}>
                    Logout
                </Button>
            </Menu.Item>
        </Menu>
    );
}

export default CandidateNavbar;