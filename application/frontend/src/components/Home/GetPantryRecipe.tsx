import React, { useState, useEffect } from "react";
import RecipeCards from "./RecipeCards";
import NavigationBar from "../NavigationBar";
import { RecipePreview } from "./Home";
import "../../styles/Home.css";
import { Container, Row } from "react-bootstrap";
import { useAuth } from "../Context/AuthContext";
import { loadingGif } from "../../constants";

const PantryRecipes: React.FC = () => {
  const { userInfo, isLoggedIn } = useAuth();
  const userId = userInfo ? userInfo.userId : 0;
  const [recipes, setRecipes] = useState<RecipePreview[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await fetch(
          `${VITE_API_URL}/api/recipe/pantry/${userId}`
        );
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        if (data.statusCode === 0) {
          setRecipes(data.data);
        } else {
          console.error("Failed to fetch recipes:", data.statusMessage);
          setRecipes([]);
        }
      } catch (error) {
        console.error("Failed to fetch recipes:", error);
        setRecipes([]);
      } finally {
        setIsLoading(false); // Set loading state to false when fetching is complete
      }
    };
    fetchRecipes();
  }, [userId]);

  return (
    <>
      <NavigationBar />

      <Container className="mt-4">
        <Row>
          <h1 className="text-center mb-5 home-header">
            RECIPES MATCH YOUR PANTRY
          </h1>
          <div style={{ display: "flex", justifyContent: "center" }}>
          {isLoading && (
            <img
              src={loadingGif}
              style={{ width: "25%" }} // Adjust these values to scale the image
              alt="Loading..."
            />
          )}
        </div>

          {!isLoading && recipes.length === 0 ? (
            <div className="empty-pantry-message">
              Your pantry is still empty. Please add ingredients to get your recipes.
            </div>
          ) : (
            !isLoading && <RecipeCards recipesList={recipes} needMask={true} />
          )}
        </Row>
      </Container>
    </>
  );
};

export default PantryRecipes;
