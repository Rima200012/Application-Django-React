import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Form, Input, Button, Select, Typography, Divider, message } from "antd";
import api from "../api";
import "../styles/Form.css";

const { Title } = Typography;
const { Option } = Select;

function RegisterForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (values) => {
    const userData = {
      username: values.username,
      password: values.password,
      email: values.email,
      role: values.role,
    };
    try {
      await api.post("/users/create/", userData);
      message.success('Registration successful!');
      navigate("/login");
    } catch (error) {
      message.error("Registration failed: " + error.message);
    }
  };

  return (
    <div className="form-container">
      <Form className="Form" onFinish={handleSubmit}>
        <Title level={2}>Register</Title>
        <Form.Item
          name="username"
          label="Username"
          rules={[{ required: true, message: 'Please enter your username!' }]}
        >
          <Input placeholder="Enter your username" />
        </Form.Item>
        <Form.Item
          name="email"
          label="Email"
          rules={[{ required: true, message: 'Please enter your email!' }]}
        >
          <Input placeholder="Enter your email" />
        </Form.Item>
        <Form.Item
          name="password"
          label="Password"
          rules={[{ required: true, message: 'Please enter your password!' }]}
        >
          <Input.Password placeholder="Enter your password" />
        </Form.Item>
        <Form.Item
          name="role"
          label="Role"
          rules={[{ required: true, message: 'Please select your role!' }]}
        >
          <Select placeholder="Select Role" onChange={(value) => setRole(value)}>
            <Option value="recruiter">Recruiter</Option>
            <Option value="candidate">Candidate</Option>
          </Select>
        </Form.Item>
        <Button type="primary" htmlType="submit" className="form-button">
          Register
        </Button>
        <Divider style={{ borderColor: "black" }}>
          Already have an account? <Link to="/login">Login Now</Link>
        </Divider>
      </Form>
    </div>
  );
}

export default RegisterForm;
