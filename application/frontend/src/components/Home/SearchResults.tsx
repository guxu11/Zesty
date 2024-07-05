import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import RecipeCards from "./RecipeCards";
import NavigationBar from "../NavigationBar";
import { RecipePreview } from "./Home";
import "../../styles/Home.css";
import { Container, Row } from "react-bootstrap";
import { loadingGif } from "../../constants";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const SearchResults: React.FC = () => {
  const [recipes, setRecipes] = useState<RecipePreview[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  let query = useQuery();

  useEffect(() => {
    setIsLoading(true);
    const input = query.get("q");
    const fetchRecipes = async () => {
      try {
        const response = await fetch(
          `${VITE_API_URL}/api/recipe/search?q=${input}`
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
        setIsLoading(false);
      }
    };

    if (input) {
      fetchRecipes();
    }
  }, [query.get("q")]);

  return (
    <>
      <NavigationBar />
      <Container className="mt-4">
        <Row>
          <h1 className="text-center mb-5 home-header">SEARCHING RESULTS</h1>

          {/* Show the loading animation while searching */}
          {isLoading ? (
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                width: "100%",
              }}
            >
              <img
                src={loadingGif}
                style={{ width: "25%" }} // Adjust these values to scale the image
                alt="Loading..."
              />
            </div>
          ) : (
            /* If not loading, show recipes or empty message */
            <>
              {recipes.length === 0 ? (
                <div className="empty-pantry-message">
                  No recipes found. Please search with other keywords.
                </div>
              ) : (
                <RecipeCards recipesList={recipes} needMask={false} />
              )}
            </>
          )}
        </Row>
      </Container>
    </>
  );
};

export default SearchResults;
