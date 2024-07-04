import React from "react";
import { Layout, Menu } from "antd";
import { NavLink, useNavigate } from "react-router-dom";
import { HiOutlinePlusCircle, HiOutlineDocument, HiOutlineUser, HiOutlineUsers, HiOutlineLogout } from "react-icons/hi";

const { Sider } = Layout;

const navItems = [
  {
    key: "add-job-post",
    icon: <HiOutlinePlusCircle size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/add-job-post`}>
        Add Job Post
      </NavLink>
    ),
  },
  {
    key: "manage-job-posts",
    icon: <HiOutlineDocument size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/manage-job-posts`}>
        Manage Job Posts
      </NavLink>
    ),
  },
  {
    key: "manage-profile",
    icon: <HiOutlineUser size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/manage-profile`}>
        Manage Profile
      </NavLink>
    ),
  },
  {
    key: "view-applicants",
    icon: <HiOutlineUsers size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/view-applicants`}>
        View Applicants
      </NavLink>
    ),
  },
  {
    key: "manage-applications",
    icon: <HiOutlineDocument size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/manage-applications`}>
        Manage Applications
      </NavLink>
    ),
  },
];

function RecruiterSidebar({ collapsed }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <Sider width={"250px"} collapsible collapsed={collapsed} style={{ minHeight: "100vh" }}>
      <Menu
        mode="inline"
        defaultSelectedKeys={["1"]}
        defaultOpenKeys={["sub1"]}
        style={{ height: "100%", borderRight: 0 }}
        items={navItems}
      />
      <Menu
        mode="inline"
        style={{ position: 'absolute', bottom: 0, width: '100%' }}
      >
        <Menu.Item key="logout" icon={<HiOutlineLogout size={18} />}>
          <a onClick={handleLogout}>Logout</a>
        </Menu.Item>
      </Menu>
    </Sider>
  );
}

export default RecruiterSidebar;
