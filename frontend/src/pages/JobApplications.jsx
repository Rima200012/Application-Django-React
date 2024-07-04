import React, { useEffect, useState } from "react";
import { Table, Button, message } from "antd";
import api from "../api";
import { useParams } from "react-router-dom";

function JobApplications() {
  const { jobId } = useParams();
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const res = await api.get(`/Jobs/jobposts/${jobId}/applications`);
        if (res.status === 200) {
          setApplications(res.data);
        } else {
          message.error("Failed to fetch applications");
        }
      } catch (error) {
        console.error("Failed to fetch applications:", error);
        message.error("Failed to fetch applications");
      }
    };

    fetchApplications();
  }, [jobId]);

  const columns = [
    {
      title: "Applicant Name",
      dataIndex: "applicant_name",
      key: "applicant_name",
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
    },
    {
      title: "Resume",
      dataIndex: "resume",
      key: "resume",
      render: (text) => <a href={text} target="_blank" rel="noopener noreferrer">View Resume</a>,
    },
    // Add more columns as needed
  ];

  return (
    <div style={{ maxWidth: 1000, margin: "0 auto", padding: "20px" }}>
      <h1>Job Applications</h1>
      <Table dataSource={applications} columns={columns} rowKey="_id" />
    </div>
  );
}

export default JobApplications;
