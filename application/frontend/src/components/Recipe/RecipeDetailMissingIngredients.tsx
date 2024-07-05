import React, { useEffect, useState } from "react";
import {
  useParams,
  useRevalidator,
  useNavigate,
  Navigate,
} from "react-router-dom";
import { Container, ListGroup, Button, Form, Card } from "react-bootstrap";
import { BsStarFill, BsStar, BsHeartFill, BsHeart } from "react-icons/bs";
import NavigationBar from "../NavigationBar";
import { useAuth } from "../Context/AuthContext";
import CommentsSection from "../CommentsSection";
import "../../styles/CommentsSection.css"; // Make sure to import the CSS for styling
import { loadingGif } from "../../constants";

interface Review {
  reviewId: number | undefined;
  userName: string;
  email: string | undefined;
  comment: string;
  rating: number;
}
interface Step {
  stepImg: string;
  stepDesc: string;
}

interface NutritionFacts {
  calories: number;
  fat: string;
}

interface Ingredient {
  ingredientId: number;
  ingredientName: string;
  category: number;
  amount: string;
  createTime: string;
  modifyTime: string;
  nutrition: null;
}

interface RecipeDetail {
  recipeId: number;
  recipeName: string;
  rating: number; // average rating
  cookingTime: string;
  steps: Step[];
  nutritionFacts: NutritionFacts;
  ingredients: Ingredient[];
  reviews: Review[];
  description: string;
  recipePicture: string;
}

interface Styles {
  container: React.CSSProperties;
  heading: React.CSSProperties;
  rating: React.CSSProperties;
  starContainer: React.CSSProperties;
  likeButton: React.CSSProperties;
  card: React.CSSProperties;
}

const styles: Styles = {
  container: {
    backgroundColor: "#fff",
    padding: "20px",
    borderRadius: "10px",
    maxWidth: "900px",
    margin: "auto",
    marginTop: "20px",
    border: "none",
  },
  heading: {
    textAlign: "center",
    marginBottom: "20px",
  },
  rating: {
    fontSize: "24px",
  },
  starContainer: {
    marginRight: "auto",
    color: "orange",
  },
  likeButton: {
    marginLeft: "10px",
    float: "right",
    marginBottom: "20px",
  },
  card: {
    marginBottom: "10px",
  },
};

const RecipeDetailPage: React.FC = () => {
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
  const { recipeId } = useParams<{ recipeId: string }>();
  const [recipeDetail, setRecipeDetail] = useState<RecipeDetail | null>(null);
  const [liked, setLiked] = useState<boolean>(false);
  const [rating, setRating] = useState<number>(0); // user rating
  const [comment, setComment] = useState<string>("");
  const [comments, setComments] = useState<Review[]>([]);
  const navigate = useNavigate();
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const [missingIngredients, setMissingIngredients] = useState<Ingredient[]>([]); // State to hold missing ingredients


  useEffect(() => {
    const fetchRecipeDetail = async () => {
      try {
        const response = await fetch(`${VITE_API_URL}/api/recipe/${recipeId}`);
        if (!response.ok) {
          throw new Error("Failed to fetch");
        }
        const data = await response.json();
        if (data.statusCode === 0) {
          setRecipeDetail(data.data);
          setComments(data.data.reviews);
          try {
            const response = await fetch(
              `${VITE_API_URL}/api/recipe/favorite/status`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  recipeId: recipeId,
                  userId: userId,
                }),
              }
            );
            if (!response.ok) {
              throw new Error("Failed to fetch");
            }
            const data = await response.json();
            if (data.statusCode === 0) {
              setLiked(data.data.status === 1);
            } else {
              console.error(
                "Failed to fetch favorite status:",
                data.statusMessage
              );
              // setLiked(false);
            }
          } catch (error) {
            console.error("Failed to fetch favorite status:", error);
            setLiked(false);
          }
        } else {
          console.error("Failed to fetch recipe detail:", data.statusMessage);
          setRecipeDetail(null);
        }
        if (isLoggedIn) {
          try {
            const response = await fetch(
              `${VITE_API_URL}/api/recipe/${recipeId}/${userId}/missingingredients`
            );
            if (!response.ok) {
              throw new Error("Failed to fetch missing ingredients");
            }
            const data = await response.json();
            if (data.statusCode === 0) {
              setMissingIngredients(data.data.missing_ingredients);
              console.log("Missing Ingredients:", data.data.missing_ingredients);
            } else {
              console.error("Failed to fetch missing ingredients:", data.statusMessage);
            }
          } catch (error) {
            console.error("Failed to fetch missing ingredients:", error);
            const mockMissingIngredients: Ingredient[] = [
              {
                ingredientId: 10,
                ingredientName: "Salt",
                category: 3,
                amount: "1 tsp",
                createTime: "2024-03-19T20:02:44",
                modifyTime: "2024-03-19T20:02:44",
                nutrition: null,
              },
              {
                ingredientId: 11,
                ingredientName: "Black Pepper",
                category: 3,
                amount: "1 tsp",
                createTime: "2024-03-19T20:05:45",
                modifyTime: "2024-03-19T20:05:45",
                nutrition: null,
              },
            ];
            setMissingIngredients(mockMissingIngredients);
            console.log("Missing Ingredients:");
          }
        }
      } catch (error) {
        console.error("API request failed. Using mock data instead:", error);
        // use mock data
        const recipeDetailMock: RecipeDetail = {
          recipeId: 1,
          recipeName: "Chef John's Nashville Hot Chicken",
          rating: 4.0,
          recipePicture:
            "https://www.allrecipes.com/thmb/9HgP6ptAydgLGFG8T9G3fKRiiKo=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/254804-chef-johns-nashville-hot-chicken-ddmfs-step1-0153-4x3-9253eda6c3b2485b8205277b36474d1c.jpg",
          cookingTime: "180 minutes",
          steps: [
            {
              stepDesc: "Arrange chicken pieces in a large bowl.",
              stepImg: "",
            },
            {
              stepDesc:
                "Whisk buttermilk, pickle brine, hot sauce, and egg together in a mixing bowl. Pour marinade over chicken and stir to ensure each piece is thoroughly coated. Cover and let chicken marinate in refrigerator 2 to 4 hours.",
              stepImg:
                "https://www.allrecipes.com/thmb/9HgP6ptAydgLGFG8T9G3fKRiiKo=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/254804-chef-johns-nashville-hot-chicken-ddmfs-step1-0153-4x3-9253eda6c3b2485b8205277b36474d1c.jpg",
            },
            // add more steps
          ],
          nutritionFacts: {
            calories: 1115,
            fat: "66g",
          },
          ingredients: [
            {
              ingredientId: 1,
              ingredientName: "whole chicken",
              category: 1,
              amount: "1",
              createTime: "2024-03-19T20:02:44",
              modifyTime: "2024-03-19T20:02:44",
              nutrition: null,
            },
            {
              ingredientId: 5,
              ingredientName: "buttermilk",
              category: 5,
              amount: "1",
              createTime: "2024-03-19T20:05:45",
              modifyTime: "2024-03-19T20:05:45",
              nutrition: null,
            },
            {
              ingredientId: 6,
              ingredientName: "pickle brine",
              category: 9,
              amount: "1",
              createTime: "2024-03-19T20:05:45",
              modifyTime: "2024-03-19T20:05:45",
              nutrition: null,
            },
            // add more ingredients
          ],
          reviews: [],
          description:
            "This is a great recipe for authentic Nashville Hot Chicken. Serve with pickles and white bread for a classic Nashville Hot Chicken meal.",
        };
        setRecipeDetail(recipeDetailMock);
      }
    };

    fetchRecipeDetail();
  }, [recipeId, isLoggedIn]);

  const handleLikeClick = async () => {
    if (!isLoggedIn) {
      setShouldRedirect(true);
      return;
    }
    try {
      const response = await fetch(`${VITE_API_URL}/api/recipe/favorite`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          recipeId: recipeId,
          userId: userId,
          status: liked ? 1 : 0,
        }),
      });
      if (!response.ok) {
        throw new Error("Failed to fetch");
      }
      const data = await response.json();
   
      if (data.statusCode === 0) {
        setLiked(!liked);
     
      } else {
        console.error("Failed to fetch favorite status:", data.statusMessage);
        setLiked(false);
      }
    } catch (error) {
      setLiked(false);
      console.error("Failed to like recipe:", error);
    }
  };

  const handleStarClick = async (index: number) => {
    setRating(index + 1);
  };

  const handleCommentSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!isLoggedIn) {
      setShouldRedirect(true);
      return;
    }
    try {
      // Send comment and rating to the backend
      const response = await fetch(`${VITE_API_URL}/api/recipe/review`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId: userId,
          recipeId: recipeId,
          comment: comment,
          rating: rating,
        }),
      });
      if (!response.ok) {
        throw new Error("Failed to submit comment");
      }
      let reviewId = 0;
      const data = await response.json();
      if (data.statusCode !== 0) {
        throw new Error("Failed to submit comment");
      } else {
        reviewId = 0;
      }
      // Update submitted comment and rating after submission
      // Add new comment to the comments array
      setComments([
        {
          userName: userName,
          comment: comment,
          rating: rating,
          email: email || "",
          reviewId: 0,
        },
        ...comments,
      ]);
      // Clear comment and reset rating after submission
      setComment("");
      setRating(0);
    } catch (error) {
      // Clear comment and reset rating after submission
      setComment("");
      setRating(0);
      console.error("Failed to submit comment:", error);
    }
  };

  if (!recipeDetail) {
    return <p>loading...</p>;
  }
  if (shouldRedirect) {
    return (
      <Navigate
        to="/login"
        state={{ from: { pathname: location.pathname } }}
        replace
      />
    );
  }
  return (
    <>
      <NavigationBar />
      <Container style={styles.container}>
        <h1 style={{ ...styles.heading, fontWeight: "bold" }}>
          {recipeDetail.recipeName}
        </h1>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            marginBottom: "20px",
            color: "orange",
          }}
        >
          <span style={{ fontSize: "24px" }}>
            {[...Array(Math.floor(recipeDetail.rating))].map((_, index) => (
              <BsStarFill key={index} />
            ))}
            {recipeDetail.rating % 1 !== 0 && <BsStarFill />}{" "}
            {recipeDetail.rating.toFixed(1)}&nbsp;
          </span>
        </div>

        <p className="recipe-description">{recipeDetail.description}</p>
        {recipeDetail && (
          <div>
            <img
              src={recipeDetail.recipePicture}
              alt="Recipe Picture"
              style={{ width: "100%", height: "auto" }}
            />
          </div>
        )}
        <div style={{ marginBottom: "30px" }}></div>

        {/* Ingredients */}
        <h3 className="step-title">Ingredients - {missingIngredients.length} / {recipeDetail.ingredients.length} missing</h3>
        <ul className="ingredient-list">
          {recipeDetail.ingredients.map((ingredient) => {
            // Check if the ingredient is missing
            const missingNames = missingIngredients.map((ingredient) => ingredient.ingredientName);
            const isMissing = missingNames.includes(ingredient.ingredientName);
            return (
              <li key={ingredient.ingredientId}>
                <span className="ingredient-info">
                  {ingredient.amount} {ingredient.ingredientName}
                </span>
                {isMissing && <span className="missing-label">Missing</span>}
              </li>
            );
          })}
        </ul>
        <h3 className="step-title">Cooking Time</h3>

        <p className="cooking-time">{recipeDetail.cookingTime}</p>
        {/* <h3 className="step-title">Nutrition Facts</h3>
        <p className="cooking-time">Calories : {recipeDetail.nutritionFacts.calories}
          <br /> Fat : {recipeDetail.nutritionFacts.fat}</p> */}

        {/* Steps */}
        <h3 className="step-title">Steps</h3>
        <ol className="step-list">
          {recipeDetail.steps.map((step, index) => (
            <li key={index}>
              {step.stepDesc}
              <br></br>
              {step.stepImg && (
                <>
                  <img
                    src={step.stepImg}
                    alt="Step Image"
                    className="step-image"
                  />
                </>
              )}
            </li>
          ))}
        </ol>

        <div style={{ marginBottom: "60px" }}></div>

        {/* Like Button */}

        <div style={{ marginBottom: "80px" }}>
          <Button
            variant="danger"
            onClick={handleLikeClick}
            style={styles.likeButton}
          >
            {liked ? <BsHeartFill size={20} /> : <BsHeart size={20} />}
            &nbsp;Like
          </Button>
        </div>
        <br></br>
        {/* Comment Form */}
        <h3 className="step-title">Reviews</h3>
        <Form onSubmit={handleCommentSubmit}>
          <Form.Group controlId="comment">
            <Form.Label>Leave a review and rating!</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              required
            />
          </Form.Group>
          {/* Star Rating */}
          <div style={{ ...styles.starContainer, fontSize: "30px" }}>
            {[...Array(5)].map((_, index) => (
              <span
                key={index}
                onClick={() => handleStarClick(index)}
                className="star-hover"
              >
                {index < rating ? <BsStarFill /> : <BsStar />}
              </span>
            ))}
            <Button variant="secondary" type="submit" className="submit-btn">
              Submit
            </Button>
          </div>
        </Form>

        <CommentsSection comments={comments} />
        {/* Submitted Comment and Rating */}
      </Container>
    </>
  );
};

export default RecipeDetailPage;
