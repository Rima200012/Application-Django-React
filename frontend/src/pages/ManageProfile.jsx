import React, { useEffect, useState, useCallback } from 'react';
import { Form, Input, Button, message, Switch } from 'antd';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { useAuth } from '../context/AuthContext';

const ManageProfile = () => {
  const { authState } = useAuth();
  const [profileData, setProfileData] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfileData = async () => {
      if (authState.authenticated) {
        try {
          const res = await api.get('/users/users/me/', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access')}`,
            },
          });
          if (res.status === 200) {
            setProfileData(res.data.user);
          } else {
            message.error('Failed to fetch profile data');
          }
        } catch (error) {
          console.error('Failed to fetch profile data:', error);
          message.error('Failed to fetch profile data');
        }
      } else {
        console.error('User is not authenticated');
      }
      setLoading(false);
    };

    fetchProfileData();
  }, [authState]);

  const handleUpdateProfile = async (values) => {
    try {
      const res = await api.put('/users/users/me/', values, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      });
      if (res.status === 200) {
        message.success('Profile updated successfully');
        setProfileData(res.data.user);
      } else {
        message.error('Failed to update profile');
      }
    } catch (error) {
      console.error('Failed to update profile:', error);
      message.error('Failed to update profile');
    }
  };

  const handleChangePassword = async (values) => {
    try {
      const res = await api.put('/users/password/', values, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      });
      if (res.status === 200) {
        message.success('Password changed successfully');
      } else {
        message.error('Failed to change password');
      }
    } catch (error) {
      console.error('Failed to change password:', error);
      message.error('Failed to change password');
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="view-host user-profile">
      <div className="view-wrapper">
        <Form
          layout="vertical"
          initialValues={profileData}
          onFinish={handleUpdateProfile}
        >
          <h1>Manage Profile</h1>
          <Form.Item
            name="username"
            label="Username"
            rules={[{ required: true, message: 'Please input your username!' }]}
          >
            <Input placeholder="Username" />
          </Form.Item>
          <Form.Item
            name="email"
            label="Email"
            rules={[{ required: true, message: 'Please input your email!' }]}
          >
            <Input placeholder="Email" readOnly />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Update Profile
            </Button>
          </Form.Item>
        </Form>

        <Form
          layout="vertical"
          onFinish={handleChangePassword}
        >
          <h1>Change Password</h1>
          <Form.Item
            name="old_password"
            label="Current Password"
            rules={[{ required: true, message: 'Please input your current password!' }]}
          >
            <Input.Password placeholder="Current Password" />
          </Form.Item>
          <Form.Item
            name="new_password"
            label="New Password"
            rules={[{ required: true, message: 'Please input your new password!' }]}
          >
            <Input.Password placeholder="New Password" />
          </Form.Item>
          <Form.Item
            name="confirm_password"
            label="Confirm New Password"
            rules={[{ required: true, message: 'Please confirm your new password!' }]}
          >
            <Input.Password placeholder="Confirm New Password" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Change Password
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default ManageProfile;

