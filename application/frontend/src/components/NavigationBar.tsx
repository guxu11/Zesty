import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import { Link } from "react-router-dom";
import "../styles/NavigationBar.css";
import React, { useState } from "react";
import SearchBar from "./SearchBar";
import { Col, InputGroup, FormControl, Button } from "react-bootstrap";
import { useAuth } from "./Context/AuthContext";
import Logo  from "../assets/zesty_h.png"

const NavigationBar: React.FC = () => {
  const { isLoggedIn, userInfo, setIsLoggedIn, setUserInfo } = useAuth();

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserInfo({
      userId: 0,
      userName: "",
      email: "",
      userType: 0
    });
    localStorage.removeItem("token"); 
    localStorage.removeItem("userInfo"); 
  };

  return (
    <Navbar expand="lg" className="navbar">
  <Container style={{ paddingLeft: '2rem', paddingRight: '2rem' }}> {/* 增加左右内边距 */}
    <Navbar.Brand className="w-20" href="/">
      {/* Zesty */}
      <img
          src={Logo} // 使用导入的 Logo 变量
          alt="Zesty Logo"
          // className="w-20"
          style={{ maxHeight: '35px', height: 'auto', width: 'auto' }}
        />
    </Navbar.Brand>

    <InputGroup className="w-45">
      <SearchBar />
    </InputGroup>

    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
      <Nav className="w-45">
        {isLoggedIn ? (
          <>
            <Nav.Item>
              <NavDropdown title={userInfo?.userName} id="basic-nav-dropdown">
                <NavDropdown.Item as={Link} to="/profile">
                  User Profile
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/create-recipe">
                  Create Recipe
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/pantry-recipes">
                  Get Your Recipe
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={handleLogout}>
                  Log out
                </NavDropdown.Item>
              </NavDropdown>
            </Nav.Item>
          </>
        ) : (
          <Nav.Item className="col-4">
            <Nav.Link as={Link} to="/login">
              Log in
            </Nav.Link>
          </Nav.Item>
        )}
        <Nav.Item className="col-4">
          <Nav.Link as={Link} to="/about" className="nav-link text-center">
            about
          </Nav.Link>
        </Nav.Item>
      </Nav>
    </Navbar.Collapse>
  </Container>
</Navbar>

  
  );
};

export default NavigationBar;
