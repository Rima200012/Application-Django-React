import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Form, Input, Button, Typography, Divider, message } from 'antd';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Form.css';

const { Title } = Typography;

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function LoginForm() {
  const query = useQuery();
  const navigate = useNavigate();
  const { login } = useAuth();

  useEffect(() => {
    if (query.get('verified') === 'true') {
      message.success('Email verified, you can log in to your account');
    }
  }, [query]);

  const handleSubmit = async (values) => {
    try {
      await login(values.email, values.password);
      const userRole = localStorage.getItem('role');
      if (userRole === 'recruiter') {
        navigate('/recruiter-home');
      } else if (userRole === 'candidate') {
        navigate('/candidate-home');
      }
    } catch (error) {
      message.error('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="form-container">
      <Form className="Form" onFinish={handleSubmit}>
        <Title level={2}>Welcome Back!</Title>
        <Form.Item
          name="email"
          label="Email"
          rules={[
            {
              required: true,
              message: 'Please enter your email!',
            },
          ]}
        >
          <Input placeholder="Enter your email" />
        </Form.Item>
        <Form.Item
          name="password"
          label="Password"
          rules={[
            {
              required: true,
              message: 'Please enter your password!',
            },
          ]}
        >
          <Input.Password placeholder="Enter your password" />
        </Form.Item>
        <Button type="primary" htmlType="submit" block>
          Login
        </Button>
        <Divider style={{ borderColor: 'black' }}>
          Don't have an account? <Link to="/register">Register Now</Link>
        </Divider>
      </Form>
    </div>
  );
}

export default LoginForm;
