// SearchJobs.jsx
import React, { useEffect, useState } from "react";
import { Card, Button, message, Row, Col, Modal, Tag } from "antd";
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
      <h1>Latest Jobs</h1>
      <Row gutter={[16, 16]}>
        {jobPosts.map((job) => (
          <Col key={job._id} xs={24} sm={24} md={24} lg={24}>
            <Card className="job-card">
              <div className="job-info">
                <div className="job-title">{job.title}</div>
                <div className="job-company">{job.company_name}</div>
                <div className="job-location">{job.location}</div>
                <div className="job-tags">
                  {job.is_active ? <Tag color="green">Active</Tag> : <Tag color="red">Inactive</Tag>}
                </div>
              </div>
              <div className="apply-button-container">
                <Button type="primary" onClick={() => showJobDetails(job)}>
                  View Details
                </Button>
              </div>
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
            selectedJob.published_by === "669560f1100fd1361bc4e49c" ? (
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
