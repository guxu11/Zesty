import React from "react";
import { Card, Col, Row, Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import "../../styles/RecipeCard.css";

interface RecipePreview {
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
  completeness?: number;
}

interface Props {
  recipesList: RecipePreview[];
  needMask?: boolean;
}

interface StarRatingProps {
  rating: number;
}

const StarRating: React.FC<StarRatingProps> = ({ rating }) => {
  const roundedRating = Math.round(rating * 2) / 2;
  return (
    <div className="star-rating">
      {[...Array(5)].map((_, index) => {
        const starValue = index + 1;
        let starClass = "far fa-star";
        if (starValue <= roundedRating) {
          starClass = "fas fa-star";
        } else if (starValue - 0.5 === roundedRating) {
          starClass = "fas fa-star-half-alt";
        }
        return <i key={index} className={starClass} />;
      })}
    </div>
  );
};

const RecipeCards: React.FC<Props> = ({ recipesList, needMask }) => {
  return (
    <Container>
      <Row>
        {recipesList.map((recipe, index) => (
          <Col key={index} xs={12} sm={6} md={4} lg={3} className="mb-4">
            <Link
              to={needMask ? `/recipe/missing/${recipe.recipeId}` : `/recipe/${recipe.recipeId}`}
              className="text-decoration-none text-dark"
            >
              <Card className="card-custom">
                <div className="card-img-wrapper">
                  <Card.Img
                    variant="top"
                    src={recipe.recipePicture}
                    className="card-img-custom"
                  />
                  {needMask && recipe.completeness && (
                    <div className="card-img-mask">
                      <div className="mask-content">
                        <span className="mask-text">
                          {recipe.completeness.toFixed(1)}%
                        </span>
                        <p className="mask-description">
                          Ingredients in Pantry
                        </p>
                      </div>
                    </div>
                  )}
                </div>
                <Card.Body className="card-body-custom">
                  <Card.Title className="card-title-custom">
                    {recipe.recipeName}
                  </Card.Title>
                  <Card.Text className="card-category-custom">
                    {recipe.category.toUpperCase()}
                  </Card.Text>
                  <div className="card-rating-custom">
                    <StarRating rating={recipe.rating} />
                  </div>
                </Card.Body>
              </Card>
            </Link>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default RecipeCards;
