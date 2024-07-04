import React, { useEffect, useState } from "react";
import { Card, Button, message, Row, Col, Modal } from "antd";
import api from "../api";
import { useNavigate } from "react-router-dom";
import "../styles/SearchJobs.css";

function SearchJobs() {
  const [jobPosts, setJobPosts] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchJobPosts = async () => {
      try {
        const res = await api.get("/Jobs/jobposts/");
        if (res.status === 200) {
          setJobPosts(res.data);
        } else {
          message.error("Failed to fetch job posts");
        }
      } catch (error) {
        console.error("Failed to fetch job posts:", error);
        message.error("Failed to fetch job posts");
      }
    };

    fetchJobPosts();
  }, []);

  const showJobDetails = (job) => {
    setSelectedJob(job);
    setIsModalVisible(true);
  };

  const handleApplyNow = (jobId) => {
    setIsModalVisible(false);
    navigate(`/candidate-home/jobposts/${jobId}/apply`);
  };

  const handleApplyExternal = (jobLink) => {
    window.open(jobLink, "_blank");
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setSelectedJob(null);
  };

  return (
    <div className="search-jobs-container">
      <h1>Job Listings</h1>
      <Row gutter={[16, 16]}>
        {jobPosts.map((job) => (
          <Col key={job._id} xs={24} sm={12} md={8} lg={6}>
            <Card title={job.title} bordered={false}>
              <p><strong>{job.title}</strong></p>
              <p>Company: {job.company_name}</p>
              <p>Location: {job.location}</p>
              <p>Status: {job.is_active ? "Active" : "Inactive"}</p>
              <Button type="primary" onClick={() => showJobDetails(job)}>
                View Details
              </Button>
            </Card>
          </Col>
        ))}
      </Row>

      {selectedJob && (
        <Modal
          title={selectedJob.title}
          visible={isModalVisible}
          onCancel={handleCancel}
          footer={[
            <Button key="cancel" onClick={handleCancel}>
              Cancel
            </Button>,
            selectedJob.published_by === "LinkedIn" ? (
              <Button key="apply" type="primary" onClick={() => handleApplyExternal(selectedJob.Job_link)}>
                Apply on LinkedIn
              </Button>
            ) : (
              <Button key="apply" type="primary" onClick={() => handleApplyNow(selectedJob._id)}>
                Apply Now
              </Button>
            )
          ]}
        >
          <p><strong>Company:</strong> {selectedJob.company_name}</p>
          <p><strong>Location:</strong> {selectedJob.location}</p>
          <p><strong>Status:</strong> {selectedJob.is_active ? "Active" : "Inactive"}</p>
          <p><strong>Description:</strong> {selectedJob.description}</p>
        </Modal>
      )}
    </div>
  );
}

export default SearchJobs;
