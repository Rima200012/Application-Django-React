import React from "react";
import { HiOutlineSearch, HiOutlineDocument, HiOutlineUser, HiOutlinePlusCircle, HiOutlineLogout } from "react-icons/hi";
import { Layout, Menu } from "antd";
import { NavLink, useNavigate } from "react-router-dom";

const { Sider } = Layout;

const navItems = [
  {
    key: "search-jobs",
    icon: <HiOutlineSearch size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/search-jobs`}>
        Search Jobs
      </NavLink>
    ),
  },
  {
    key: "my-applications",
    icon: <HiOutlineDocument size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/my-applications`}>
        My Applications
      </NavLink>
    ),
  },
  {
    key: "manage-profile",
    icon: <HiOutlineUser size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/manage-profile`}>
        My Profile
      </NavLink>
    ),
  },
  {
    key: "add-job-request",
    icon: <HiOutlinePlusCircle size={18} />,
    label: (
      <NavLink className={"activeLink"} to={`/add-job-request`}>
        Add Job Request
      </NavLink>
    ),
  },
];

function CandidateSidebar({ collapsed }) {
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

export default CandidateSidebar;
