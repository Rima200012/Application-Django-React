import React from "react";
import { Form, Input, Button, message, Switch } from "antd";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const AddJobPost = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const onFinish = async (values) => {
    try {
      // Remove published_by from the payload
      const payload = {
        ...values,
      };
      const response = await api.post("/Jobs/jobposts/", payload);
      if (response.status === 201) {
        message.success("Job post created successfully");
        navigate("/recruiter-home");
      } else {
        message.error("Failed to create job post");
      }
    } catch (error) {
      console.error("Error creating job post:", error);
      message.error("Failed to create job post");
    }
  };

  const onFinishFailed = () => {
    message.error("You have to fill in all fields");
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: "20px" }}>
      <h1>Add Job Post</h1>
      <Form
        layout="vertical"
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
      >
        <Form.Item
          name="title"
          label="Title"
          rules={[{ required: true, message: "Please input the job title!" }]}
        >
          <Input placeholder="Job Title" />
        </Form.Item>
        <Form.Item
          name="description"
          label="Description"
          rules={[{ required: true, message: "Please input the job description!" }]}
        >
          <Input.TextArea placeholder="Job Description" />
        </Form.Item>
        <Form.Item
          name="company_name"
          label="Company Name"
          rules={[{ required: true, message: "Please input the company name!" }]}
        >
          <Input placeholder="Company Name" />
        </Form.Item>
        <Form.Item
            name="location"
            label="Location"
            rules={[{ required: true, message: "Please input the location!" }]}
          >
            <Input placeholder="Location" />
          </Form.Item>
          <Form.Item
          name="Job_link"
          label="Job_link"
          rules={[{ required: false}]}
        >
          <Input placeholder="Job_link" />
        </Form.Item>
        <Form.Item
          name="is_active"
          label="Is Active"
          valuePropName="checked"
        >
          <Switch checkedChildren="Active" unCheckedChildren="Inactive" />
        </Form.Item>
        
        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            Submit
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default AddJobPost;