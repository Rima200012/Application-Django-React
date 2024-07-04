import React, { useEffect, useState } from "react";
import { Form, Input, Button, Switch, message } from "antd";
import api from "../api";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function UpdateJobPost() {
  const { jobId } = useParams(); // Assume jobId is passed as a URL parameter
  const [jobPost, setJobPost] = useState(null);
  const navigate = useNavigate();
  const { authState } = useAuth();

  useEffect(() => {
    const fetchJobPost = async () => {
      if (authState.authenticated) {
        try {
          const res = await api.get(`/Jobs/jobposts/${jobId}/`);
          

          if (res.status === 200) {
            setJobPost(res.data);
          } else {
            message.error("Failed to fetch job post");
          }
        } catch (error) {
          console.error("Failed to fetch job post:", error);
          message.error("Failed to fetch job post");
        }
      } else {
        console.error("User is not authenticated");
      }
    };

    fetchJobPost();
  }, [jobId, authState]);

  const handleUpdate = async (values) => {
    if (authState.authenticated) {
      try {
        const res = await api.put(`/Jobs/jobposts/${jobId}/`, values);
        if (res.status === 200) {
          message.success("Job post updated successfully");
          navigate("/recruiter-home");
        } else {
          message.error("Failed to update job post");
        }
      } catch (error) {
        console.error("Failed to update job post:", error);
        message.error("Failed to update job post");
      }
    } else {
      console.error("User is not authenticated");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: "20px" }}>
      <h1>Update Job Post</h1>
      {jobPost && (
        <Form
          layout="vertical"
          initialValues={jobPost}
          onFinish={handleUpdate}
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
            name="is_active"
            label="Is Active"
            valuePropName="checked"
          >
            <Switch checkedChildren="Active" unCheckedChildren="Inactive" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Update
            </Button>
          </Form.Item>
        </Form>
      )}
    </div>
  );
};

export default UpdateJobPost;
