import React, { useState } from "react";
import { Form, Input, Button, message, Upload } from "antd";
import api from "../api";
import { useAuth } from "../context/AuthContext";
import { useNavigate, useParams } from "react-router-dom";

const { TextArea } = Input;

function ApplyJob() {
  const { authState } = useAuth();
  const { jobId } = useParams(); // Assume jobId is passed as a URL parameter
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);

  const handleFileChange = (info) => {
    setResume(info.file);
  };

  const onFinish = async (values) => {
    const formData = new FormData();
    formData.append('applicant_name', values.applicant_name);
    formData.append('cover_letter', values.cover_letter);
    formData.append('job_post_id', jobId); // Add job_post_id to the form data
    formData.append('resume', resume);

    try {
      const response = await api.post("/Jobs/applications/", formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status === 201) {
        message.success("Job application submitted successfully");
        navigate("/candidate-home/my-applications");
      } else {
        message.error("Failed to submit job application");
      }
    } catch (error) {
      console.error("Error submitting application:", error);
      message.error("Failed to submit job application");
    }
  };

  const onFinishFailed = () => {
    message.error("Please fill in all fields");
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: "20px" }}>
      <h1>Apply for Job</h1>
      <Form
        layout="vertical"
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
      >
        <Form.Item
          name="applicant_name"
          label="Applicant Name"
          rules={[{ required: true, message: "Please input your name!" }]}
        >
          <Input placeholder="Applicant Name" />
        </Form.Item>
        <Form.Item
          name="cover_letter"
          label="Cover Letter"
          rules={[{ required: true, message: "Please input your cover letter!" }]}
        >
          <TextArea placeholder="Cover Letter" />
        </Form.Item>
        <Form.Item
          name="resume"
          label="Upload Resume"
          rules={[{ required: true, message: "Please upload your resume!" }]}
        >
          <Upload
            beforeUpload={() => false}
            onChange={handleFileChange}
          >
            <Button>Click to Upload</Button>
          </Upload>
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            Submit Application
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};
export default ApplyJob;

