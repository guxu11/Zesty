import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import '../styles/Login.css'; // Importing the CSS for styling

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    // repassword: "",
  });

  let navigate = useNavigate();
  const [passwordShown, setPasswordShown] = useState(false);
  const togglePasswordVisibility = () => {
    setPasswordShown(!passwordShown);
  };
  // const [passwordsMatch, setPasswordsMatch] = useState(true); // State to track if passwords match
  const [errorMessage, setErrorMessage] = useState(""); // State to track error message
  const [success, setSuccess] = useState(false); // State to track registration success

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Check if the password matches the re-entered password
    // if (formData.password !== formData.repassword) {
    //   alert("Passwords do not match!");
    //   setPasswordsMatch(false);
    //   return; // Stop form submission if passwords do not match
    // }

    // setPasswordsMatch(true);
    // Passwords match, proceed with form submission
    console.log("Form submitted:", formData);
    // Add code here to handle form submission, such as sending data to server
    // You can perform form validation here before submitting the data
    try {
      const response = await fetch(`${VITE_API_URL}/api/user/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.username,
          email: formData.email,
          password: formData.password,
        }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log("Response from server:", data);
      // Handle response from server as needed
      if (data.statusCode === 0) {
        // Registration success
        setSuccess(true);
        navigate("/login");
      } else if (data.statusCode === 100100) {
        // Show error message if statusCode is 100100
        setErrorMessage("Email already exists.");
      }
    } catch (error) {
      console.error("Error:", error);
      const mockData = {
        statusCode: 0,
        statusMessage: "success",
      };
      setErrorMessage(mockData.statusMessage);
      setSuccess(true);
      navigate("/login");
    }
  };

  return (
    <div className="login-container">
    <div className="login-form">
      <h2 className="text-center mb-4">Register</h2>
      <form onSubmit={handleSubmit}>
      <div className="form-group mb-3">
          <label htmlFor="email">Username:</label>
          <input type="text" className="form-control" id="username" name="username" value={formData.username} onChange={handleChange} required />
        </div>
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
        <button type="submit" className="btn btn-primary w-100">Register</button>
      </form>
      <div className="text-center mt-4">
        Already have an account? <Link to="/login" className="join-now-link">Login</Link>
      </div>
    </div>
  </div>

  );
};

export default Register;
