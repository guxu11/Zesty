// CreateRecipePage.tsx

import React, { useState, useEffect } from "react";
import { useAuth } from "../Context/AuthContext";
import { Link, useNavigate } from "react-router-dom";
import NavigationBar from "../NavigationBar";
import { BiTrash } from "react-icons/bi";
import "bootstrap/dist/css/bootstrap.min.css";
import { Card, Col, Row, Container, Button } from "react-bootstrap";
import PantryList from "./PantryList";
import { RecipePreview } from "../Home/Home";
import RecipeCards from "../Home/RecipeCards";

// Define the CreateRecipePage component
const Profile: React.FC = () => {
  const { userInfo, isLoggedIn } = useAuth();
  let userId = 0;
  let email = "";
  let userName = "";
  if (userInfo === null) {
    userId = 0;
    email = "";
    const userName = "";
  } else {
    userId = userInfo.userId;
    email = userInfo.email;
    userName = userInfo.userName;
  }
  const [userPostRecipes, setUserPostRecipes] = useState<RecipePreview[]>([]);
  const [userLikesRecipes, setUserLikesRecipes] = useState<RecipePreview[]>([]);
 

  useEffect(() => {
    const fetchUserPostRecipe = async () => {
      try {
        const response = await fetch(
          `${VITE_API_URL}/api/user/${userId}/recipes`
        );
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        console.log(data.statusCode);
        if (data.statusCode === 0) {
          setUserPostRecipes(data.data);
          console.log(data.data);
        } else {
          console.error("Failed to fetch recipes:", data.statusMessage);
          throw new Error(data.statusMessage);
        }
      } catch (error) {
        console.error("Failed to fetch recipes, using mock data:", error);
        // 使用 mock 数据更新状态
      }
    };
    fetchUserPostRecipe();
  }, []);

  useEffect(() => {
    const fetchUserLikesRecipe = async () => {
      try {
        const response = await fetch(
          `${VITE_API_URL}/api/user/${userId}/favorite`
        );
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        console.log(data.statusCode);
        if (data.statusCode === 0) {
          setUserLikesRecipes(data.data);
          console.log(data.data);
        } else {
          console.error("Failed to fetch recipes:", data.statusMessage);
          throw new Error(data.statusMessage);
        }
      } catch (error) {
        console.error("Failed to fetch recipes, using mock data:", error);
      }
    };
    fetchUserLikesRecipe();
  }, []);

  if (!isLoggedIn) {
    // Redirect to login page if not logged in
    const navigate = useNavigate();
    navigate("/login");
    return null;
  }

  // JSX template for the component
  return (
    <>
      <NavigationBar />
      <Container>
        <Col className="mx-auto" lg={9}>
          <div className="text-center">
            <h2 className="mt-3">Hello {userName}</h2>
          </div>

          <hr />

          <Container id="user-patry">
            <Row>
              <div className="text-center">
                <h4 className="mt-3">Pantry</h4>
              </div>
            </Row>
            <PantryList userId={userId}  />
          </Container>

          <hr />

          <Container id="user-post">
            <Row>
              <div className="text-center">
                <h4 className="mt-3">Posts</h4>
              </div>
            </Row>
            <RecipeCards recipesList={userPostRecipes} />
          </Container>

          <hr />

          <Container id="user-like-recipe">
            <Row>
              <div className="text-center">
                <h4 className="mt-3">Likes</h4>
              </div>
            </Row>
            <RecipeCards recipesList={userLikesRecipes} />
          </Container>

          <hr />
        </Col>
      </Container>
    </>
  );
};

// Export the CreateRecipePage component
export default Profile;
