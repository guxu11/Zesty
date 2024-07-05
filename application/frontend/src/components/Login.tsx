import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "./Context/AuthContext"; // Make sure the path is correct
import '../styles/Login.css'; // Importing the CSS for styling

const Login: React.FC = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [passwordShown, setPasswordShown] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  console.log("state", location.state); // 调试输出，看看state中有什么
  const { setIsLoggedIn, setUserInfo } = useAuth();
  const from = location.state?.from?.pathname || "/";

  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const togglePasswordVisibility = () => {
    setPasswordShown(!passwordShown);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log("Form submitted:", formData);
    
    try {
      const response = await fetch(`${VITE_API_URL}/api/user/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.statusMessage || response.statusText);
      }

      if (data.statusCode === 0) {
        setIsLoggedIn(true);
        setUserInfo({
          userId: data.data.userId,
          userName: data.data.userName,
          email: data.data.email,
          userType: data.data.userType,
        });
        console.log("Last page:", from);
        navigate(from, { replace: true });
      } else {
        setErrorMessage(data.statusMessage || "An error occurred");
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error("Login error:", error);
        setErrorMessage(error.message);
      } else {
        console.error("Login error:", error);
        setErrorMessage("An error occurred");
      }
      navigate("/login");
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2 className="text-center mb-4">Log in</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group mb-3">
            <label htmlFor="email">Email:</label>
            <input type="email" className="form-control" id="email" name="email" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-group mb-3">
            <label htmlFor="password">Password:</label>
            <div className="password-wrapper">
              <input type={passwordShown ? "text" : "password"} className="form-control" id="password" name="password" value={formData.password} onChange={handleChange} required />
              <span className="password-toggle" onClick={togglePasswordVisibility}>
                {passwordShown ? "Hide" : "Show"}
              </span>
            </div>
          </div>
          {errorMessage && <div className="alert alert-danger" role="alert">{errorMessage}</div>}
          <button type="submit" className="btn btn-primary w-100">Login</button>
        </form>
        <div className="text-center mt-4">
          Don't have an account? <Link to="/register" className="join-now-link">Join now</Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
