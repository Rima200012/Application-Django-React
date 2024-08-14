import React, { useEffect, useState } from "react";
import { Table, Button, message, Popconfirm, Modal, Spin } from "antd";
import api from "../api";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../styles/ManageJobPosts.css"; // Import the CSS file for custom styles

function ManageJobPosts() {
  const { authState } = useAuth();
  const [jobPosts, setJobPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [applicants, setApplicants] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [isResumeModalVisible, setIsResumeModalVisible] = useState(false);
  const [resumeUrl, setResumeUrl] = useState("");
  const [applicantCounts, setApplicantCounts] = useState({});
  const [recommendations, setRecommendations] = useState([]);
  const [recommendationModalVisible, setRecommendationModalVisible] = useState(false);
  const [resumePdfUrl, setResumePdfUrl] = useState("");
  const [lastSavedRecommendations, setLastSavedRecommendations] = useState([]);
  const [lastSavedRecommendationModalVisible, setLastSavedRecommendationModalVisible] = useState(false);
  const [noSavedRecommendationsMessage, setNoSavedRecommendationsMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchJobPosts = async () => {
      if (authState.authenticated) {
        try {
          const userRes = await api.get("/users/users/me/", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          });
          const userId = userRes.data.user.id;

          const jobPostsRes = await api.get("/Jobs/jobposts/", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          });

          if (jobPostsRes.status === 200) {
            const userJobPosts = jobPostsRes.data.filter(post => post.published_by === userId);
            // Fetch applicant counts for each job post
          const applicantCountsRes = await Promise.all(
            userJobPosts.map(async (post) => {
              const countRes = await api.get(`/Jobs/jobposts/${post._id}/applications/count/`, {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem("access")}`,
                },
              });
              return { jobId: post._id, count: countRes.data.count };
            })
          );

          const counts = applicantCountsRes.reduce((acc, { jobId, count }) => {
            acc[jobId] = count;
            return acc;
          }, {});

          setApplicantCounts(counts);
          setJobPosts(userJobPosts);
          } else {
            message.error("Failed to fetch job posts");
          }
        } catch (error) {
          console.error("Failed to fetch job posts:", error);
          message.error("Failed to fetch job posts");
        } finally {
          setLoading(false);
        }
      } else {
        console.error("User is not authenticated");
        setLoading(false);
      }
    };

    fetchJobPosts();
  }, [authState]);

  const handleDelete = async (id) => {
    try {
      const res = await api.delete(`/Jobs/jobposts/${id}`);
      if (res.status === 204) {
        setJobPosts(jobPosts.filter(post => post._id !== id));
        message.success("Job post deleted successfully");
      } else {
        message.error("Failed to delete job post");
      }
    } catch (error) {
      console.error("Failed to delete job post:", error);
      message.error("Failed to delete job post");
    }
  };

  const handleViewApplicants = async (jobId) => {
    setSelectedJobId(jobId);
    setModalLoading(true);
    setModalVisible(true);
    try {
      const res = await api.get(`/Jobs/jobposts/${jobId}/applications/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });

      if (res.status === 200) {
        if (res.data.message) {
          setApplicants([]);
          message.info(res.data.message);
        } else {
          setApplicants(res.data);
          setApplicantCounts((prevCounts) => ({
          ...prevCounts,
          [jobId]: res.data.length, // Update the applicant count for this job post
        }));

        }
        
      } else {
        message.error("Failed to fetch applicants");
      }
    } catch (error) {
      console.error("Failed to fetch applicants:", error);
      message.error("Failed to fetch applicants");
    } finally {
      setModalLoading(false);
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
        setResumePdfUrl(resumeUrl);
        setIsResumeModalVisible(true);
      } else {
        message.error("Failed to fetch resume");
      }
    } catch (error) {
      console.error("Failed to fetch resume:", error);
      message.error("Failed to fetch resume");
    }
  };

  const fetchRecommendations = async (jobId) => {
    setSelectedJobId(jobId);
    setRecommendationModalVisible(true);
    setModalLoading(true);
    try {
      const res = await api.get(`/AI/resume_similarity/${jobId}/`);
      if (res.status === 200) {
        if (res.data.message) {
          setRecommendations([]);
          message.info(res.data.message);
        } else {
          setRecommendations(res.data.recommendations);
        }
      } else {
        message.error("Failed to fetch recommendations");
      }
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
      message.error("Failed to fetch recommendations");
    } finally {
      setModalLoading(false);
    }
  };

  const fetchLastSavedRecommendations = async (jobId) => {
    setSelectedJobId(jobId);
    setLastSavedRecommendationModalVisible(true);
    setModalLoading(true);
    try {
      const res = await api.get(`/AI/last_saved_recommendations/${jobId}/`);
      if (res.status === 200) {
        if (res.data.message) {
          setNoSavedRecommendationsMessage(res.data.message);
          setLastSavedRecommendations([]);
        } else {
          setNoSavedRecommendationsMessage("");
          setLastSavedRecommendations(res.data.recommendations);
        }
      } else {
        message.error("Failed to fetch last saved recommendations");
      }
    } catch (error) {
      console.error("Failed to fetch last saved recommendations:", error);
      message.error("Failed to fetch last saved recommendations");
    } finally {
      setModalLoading(false);
    }
  };

  const updateStatus = async (applicationId, status) => {
    try {
      const res = await api.put(`/Jobs/applications/${applicationId}/status/`, { status }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });
      if (res.status === 200) {
        message.success("Status updated successfully");
        setApplicants(applicants.map(app => app._id === applicationId ? { ...app, status } : app));
      } else {
        message.error("Failed to update status");
      }
    } catch (error) {
      console.error("Failed to update status:", error);
      message.error("Failed to update status");
    }
  };

  const columns = [
    {
      title: "Job Title",
      dataIndex: "title",
      key: "title",
    },
    {
      title: "Company Name",
      dataIndex: "company_name",
      key: "company_name",
    },
    {
      title: "Location",
      dataIndex: "location",
      key: "location",
    },
    {
      title: "No of Applicants",
      key: "no_of_applicants",
      render: (text, record) => (
        <div>
          <Button type="link" onClick={() => handleViewApplicants(record._id)}>
            View All
          </Button>
          <span>({applicantCounts[record._id] || 0})</span> {/* Display the count */}
        </div>
      ),
    },
    {
      title: "Status",
      key: "is_active",
      render: (text, record) => (record.is_active ? "Active" : "Inactive"),
    },
    {
      title: "Reference",
      dataIndex: "_id",
      key: "reference",
    },
    {
      title: "Top 10 Best Resumes",
      key: "top_resumes",
      render: (text, record) => (
        <div>
          <Button type="link" onClick={() => fetchRecommendations(record._id)}>
            View Resumes
          </Button>
          <Button type="link" onClick={() => fetchLastSavedRecommendations(record._id)}>
            View Last Saved Resumes
          </Button>
        </div>
      ),
    },
    {
      title: "Actions",
      key: "actions",
      render: (text, record) => (
        <span>
          <Button type="link" onClick={() => navigate(`/recruiter-home/jobposts/${record._id}/update`)}>
            Update Job
          </Button>
          <Popconfirm
            title="Are you sure you want to delete this job post?"
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

  const applicantColumns = [
    {
      title: "Applicant Name",
      dataIndex: "applicant_name",
      key: "applicant_name",
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
      key: "status",
      render: (text, record) => (
        <div>
          <Button
            type={record.status === "Accepted" ? "primary" : "default"}
            style={{ backgroundColor: record.status === "Accepted" ? "green" : "", margin: '0 2px', padding: '0 4px', fontSize: '10px' }}
            onClick={() => updateStatus(record._id, "Accepted")}
          >
            Accepted
          </Button>
          <Button
            type={record.status === "Rejected" ? "primary" : "default"}
            style={{ backgroundColor: record.status === "Rejected" ? "red" : "", margin: '0 2px', padding: '0 4px', fontSize: '10px' }}
            onClick={() => updateStatus(record._id, "Rejected")}
          >
            Rejected
          </Button>
          <Button
            type={record.status === "In Progress" ? "primary" : "default"}
            style={{ backgroundColor: record.status === "In Progress" ? "yellow" : "", margin: '0 2px', padding: '0 4px', fontSize: '10px' }}
            onClick={() => updateStatus(record._id, "In Progress")}
          >
            In Progress
          </Button>
          <Button
            type={record.status === "Not Treated Yet" ? "primary" : "default"}
            style={{ backgroundColor: record.status === "Not Treated Yet" ? "blue" : "", margin: '0 2px', padding: '0 4px', fontSize: '10px' }}
            onClick={() => updateStatus(record._id, "Not Treated Yet")}
          >
            Not Treated Yet
          </Button>
        </div>
      ),
    },
  ];

  const recommendationColumns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
    },
    {
      title: "Resume ID",
      dataIndex: "resume_id",
      key: "resume_id",
      render: (resumeId) => (
        <Button type="link" onClick={() => fetchResumeDetails(resumeId)}>
          {resumeId}
        </Button>
      ),
    },
    {
      title: "Similarity Score",
      dataIndex: "similarity_score",
      key: "similarity_score",
    },
  ];

  return (
    <div style={{ maxWidth: 1000, margin: "0 auto", padding: "20px" }}>
      <h1>Manage Job Posts</h1>
      {loading ? (
        <Spin size="large" />
      ) : (
        <Table dataSource={jobPosts} columns={columns} rowKey="_id" />
      )}
      <Modal
        title="Applicants"
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={800}
      >
        {modalLoading ? (
          <Spin size="large" />
        ) : (
          <Table
            className="modal-table"
            dataSource={applicants}
            columns={applicantColumns}
            rowKey="_id"
            pagination={false} // Disable pagination to fit the modal
          />
        )}
      </Modal>
      <Modal
        title="Top 10 Best Resumes"
        visible={recommendationModalVisible}
        onCancel={() => setRecommendationModalVisible(false)}
        footer={null}
        width={800}
      >
        {modalLoading ? (
          <Spin size="large" />
        ) : (
          <Table
            className="modal-table"
            dataSource={recommendations}
            columns={recommendationColumns}
            rowKey="resume_id"
            pagination={false} // Disable pagination to fit the modal
          />
        )}
      </Modal>
      <Modal
        title="Last Saved Top 10 Best Resumes"
        visible={lastSavedRecommendationModalVisible}
        onCancel={() => setLastSavedRecommendationModalVisible(false)}
        footer={null}
        width={800}
      >
        {modalLoading ? (
          <Spin size="large" />
        ) : noSavedRecommendationsMessage ? (
          <div>{noSavedRecommendationsMessage}</div>
        ) : (
          <Table
            className="modal-table"
            dataSource={lastSavedRecommendations}
            columns={recommendationColumns}
            rowKey="resume_id"
            pagination={false} // Disable pagination to fit the modal
          />
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
        <iframe src={resumePdfUrl} width="100%" height="500px" style={{ border: 'none' }}></iframe>
      </Modal>
    </div>
  );
}

export default ManageJobPosts;
