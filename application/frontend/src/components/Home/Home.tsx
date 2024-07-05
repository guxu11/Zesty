import React, { useState, useEffect } from "react";
import { Container, Row } from "react-bootstrap";
import RecipeCards from "./RecipeCards";
import NavigationBar from "../NavigationBar";
import "../../styles/Home.css";

export interface RecipePreview {
  recipeId: number;
  recipeName: string;
  category: string;
  recipePicture?: string;
  rating: number;
  creatorId: number;
  recipeType: string;
  status: number;
  postTime: string;
  createTime: string;
  modifyTime: string;
}

const Home: React.FC = () => {
  const [recipes, setRecipes] = useState<RecipePreview[]>([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await fetch(`${VITE_API_URL}/api/recipe/random`);
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        if (data.statusCode === 0) {
          setRecipes(data.data);
        } else {
          console.error("Failed to fetch recipes:", data.statusMessage);
          throw new Error(data.statusMessage);
        }
      } catch (error) {
        console.error("Failed to fetch recipes, using mock data:", error);
        // 使用 mock 数据更新状态
        setRecipes([
          // 在这里插入你的 mock 数据
          {
            recipeId: 1,
            recipeName: "Chef John's Nashville Hot Chicken",
            category: "Dinner",
            recipePicture:
              "https://www.allrecipes.com/thmb/VpE1xykUpZ9GsVbCeQjR2oCTvME=/0x512/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/254804-chef-johns-nashville-hot-chicken-DDMFS-4x3-c1192bac5dfc43bba55056a33a17153f.jpg",
            rating: 4.0,
            creatorId: 1,
            recipeType: "1",
            status: 1,
            postTime: "2024-03-18 20:32:12",
            createTime: "2024-03-19 03:32:31",
            modifyTime: "2024-03-19 22:54:44",
          },
          // 添加更多 mock 数据项
        ]);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <>
      <NavigationBar />
      <Container className="mt-4">
        <Row>
          <h1 className="text-center mb-5 home-header">Welcome to Zesty!</h1>
          <RecipeCards recipesList={recipes} needMask={false} />
        </Row>
      </Container>
    </>
  );
};

export default Home;
