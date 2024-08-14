import React, { useEffect, useState } from "react";
import { Table, Button, message, Spin, Popconfirm, Modal } from "antd";
import api from "../api";
import { useAuth } from "../context/AuthContext";

function MyApplications() {
  const { authState } = useAuth();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isResumeModalVisible, setIsResumeModalVisible] = useState(false);
  const [resumeUrl, setResumeUrl] = useState("");
  const [jobDetails, setJobDetails] = useState(null);

  useEffect(() => {
    const fetchApplications = async () => {
      if (authState.authenticated) {
        try {
          // Fetch the authenticated user's data
          const userRes = await api.get("/users/users/me/", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          });
          const userId = userRes.data.user.id;

          // Fetch all applications by the authenticated user
          const applicationsRes = await api.get("/Jobs/applications/", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          });

          if (applicationsRes.status === 200) {
            const userApplications = applicationsRes.data.filter(app => app.added_by === userId);
            setApplications(userApplications);
          } else {
            message.error("Failed to fetch job applications");
          }
        } catch (error) {
          console.error("Failed to fetch job applications:", error);
          message.error("Failed to fetch job applications");
        }
        setLoading(false);
      } else {
        console.error("User is not authenticated");
      }
    };

    fetchApplications();
  }, [authState]);

  const handleDelete = async (id) => {
    console.log(`Deleting application with ID: ${id}`); // Debug log
    if (!id) {
      message.error('Failed to delete application: ID is undefined');
      return;
    }
    try {
      const res = await api.delete(`/Jobs/applications/${id}`);
      if (res.status === 204) {
        setApplications(applications.filter(app => app._id !== id));
        message.success("Application deleted successfully");
      } else {
        message.error("Failed to delete application");
      }
    } catch (error) {
      console.error("Failed to delete application:", error);
      message.error("Failed to delete application");
    }
  };

  const fetchJobDetails = async (jobPostId) => {
    try {
      const res = await api.get(`/Jobs/jobposts/${jobPostId}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });
      if (res.status === 200) {
        setJobDetails(res.data);
        setIsModalVisible(true);
      } else {
        message.error("Failed to fetch job details");
      }
    } catch (error) {
      console.error("Failed to fetch job details:", error);
      message.error("Failed to fetch job details");
    }
  };

  const fetchResumeDetails = async (resumeId) => {
    try {
      const res = await api.get(`/Jobs/media/${resumeId}/`, {
        responseType: 'blob', // Important for handling PDF files
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });
      if (res.status === 200) {
        const resumeUrl = URL.createObjectURL(res.data);
        setResumeUrl(resumeUrl);
        setIsResumeModalVisible(true);
      } else {
        message.error("Failed to fetch resume");
      }
    } catch (error) {
      console.error("Failed to fetch resume:", error);
      message.error("Failed to fetch resume");
    }
  };

  const getStatusMessage = (status) => {
    switch (status) {
      case "Accepted":
        return "The recruiter (or the company) will contact you soon via email.";
      case "Rejected":
        return "Your application was not successful. Please apply to other opportunities.";
      case "In Progress":
        return "Your application is currently being reviewed.";
      case "Not Treated Yet":
        return "Your application has not been reviewed yet.";
      default:
        return "";
    }
  };

  const columns = [
    {
      title: "Job ID",
      dataIndex: "job_post_id",
      key: "job_post_id",
      render: (text, record) => (
        <a onClick={() => fetchJobDetails(record.job_post_id)}>
          {record.job_post_id}
        </a>
      ),
    },
    {
      title: "Cover Letter",
      dataIndex: "cover_letter",
      key: "cover_letter",
    },
    {
      title: "Resume",
      key: "resume",
      render: (text, record) => (
        <Button type="link" onClick={() => fetchResumeDetails(record.resume)}>
          View Resume
        </Button>
      ),
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (text, record) => (
        <div>
          <p>{record.status}</p>
          <p>{getStatusMessage(record.status)}</p>
        </div>
      ),
    },
    {
      title: "Reference",
      dataIndex: "_id",
      key: "reference",
    },
    {
      title: "Actions",
      key: "actions",
      render: (text, record) => (
        <span>
          <Popconfirm
            title="Are you sure you want to delete this application?"
            onConfirm={() => handleDelete(record._id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" danger>
              Delete
            </Button>
          </Popconfirm>
        </span>
      ),
    },
  ];

  if (loading) {
    return <Spin size="large" />;
  }

  return (
    <div style={{ maxWidth: 1000, margin: "0 auto", padding: "20px" }}>
      <h1>My Applications</h1>
      <Table dataSource={applications} columns={columns} rowKey="_id" />
      <Modal
        title="Job Post Details"
        visible={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsModalVisible(false)}>
            Close
          </Button>,
        ]}
      >
        {jobDetails && (
          <div>
            <p><strong>Title:</strong> {jobDetails.title}</p>
            <p><strong>Company Name:</strong> {jobDetails.company_name}</p>
            <p><strong>Location:</strong> {jobDetails.location}</p>
            <p><strong>Description:</strong> {jobDetails.description}</p>
            <p><strong>Status:</strong> {jobDetails.is_active ? "Active" : "Inactive"}</p>
          </div>
        )}
      </Modal>
      <Modal
        title="View Resume"
        visible={isResumeModalVisible}
        onCancel={() => setIsResumeModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsResumeModalVisible(false)}>
            Close
          </Button>,
        ]}
        width="50%"
      >
        <iframe src={resumeUrl} width="100%" height="500px" style={{ border: 'none' }}></iframe>
      </Modal>
    </div>
  );
}

export default MyApplications;
