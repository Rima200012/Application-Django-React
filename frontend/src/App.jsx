import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import RecruiterHomePage from './pages/RecruiterHome';
import CandidateHomePage from './pages/CandidateHome';
import AddJobPost from './pages/AddJobPost';
import ManageJobPosts from './pages/ManageJobPosts';
import JobApplications from "./pages/JobApplications";
import UpdateJobPost from "./pages/UpdateJobPost";
import ManageProfile from './pages/ManageProfile';
import MyApplications from "./pages/MyApplications";
import SearchJobs from "./pages/SearchJobs";
import ApplyJob from "./pages/ApplyJob";
import ProtectedRoute from "./components/ProtectedRoute";
import CandidateLayout from "./components/CandidateLayout";
import RecruiterLayout from "./components/RecruiterLayout";
import { AuthProvider } from "./context/AuthContext";
import 'antd/dist/reset.css'; // Correct import for Ant Design CSS

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/register" element={<RegisterAndLogout />} />
          
          <Route path="*" element={<NotFound />} />

          {/* Candidate Routes */}
          <Route
            path="/candidate-home"
            element={
              <ProtectedRoute role="candidate">
                <CandidateLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<CandidateHomePage />} />
            <Route path="search-jobs" element={<SearchJobs />} />
            <Route path="my-applications" element={<MyApplications />} />
            <Route path="jobposts/:jobId/apply" element={<ApplyJob />} />
            <Route path="manage-profile" element={<ManageProfile />} />
          </Route>

          {/* Recruiter Routes */}
          <Route
            path="/recruiter-home"
            element={
              <ProtectedRoute role="recruiter">
                <RecruiterLayout />
                
              </ProtectedRoute>
            }
          >
            <Route index element={<RecruiterHomePage />} />
            <Route path="add-job-post" element={<AddJobPost />} />
            <Route path="manage-job-posts" element={<ManageJobPosts />} />
            <Route path="jobposts/:jobId/applicants" element={<JobApplications />} />
            <Route path="jobposts/:jobId/update" element={<UpdateJobPost />} />
            <Route path="manage-profile" element={<ManageProfile />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
