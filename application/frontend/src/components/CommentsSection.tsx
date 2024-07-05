import React from "react";
import { Card } from "react-bootstrap";
import { BsStarFill, BsStarHalf, BsStar } from "react-icons/bs";
import '../styles/CommentsSection.css'; // Make sure to import the CSS for styling


interface Review {
    reviewId: number | undefined;
    userName: string;
    email: string | undefined;
    comment: string;
    rating: number;
  }
  
  interface Props {
    comments: Review[];
  }
  
  const CommentsSection: React.FC<Props> = ({ comments }) => {
    // Function to render star icons based on rating
    const renderStars = (rating: number) => {
      // Create full stars
      const fullStars = Math.floor(rating);
      // Check if there is a half star
      const halfStar = rating % 1 >= 0.5 ? <BsStarHalf key="half-star" /> : null;
      // Create empty stars
      const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
  
      return (
        <>
          {[...Array(fullStars)].map((_, index) => (
            <BsStarFill key={`full-${index}`} />
          ))}
          {halfStar}
          {[...Array(emptyStars)].map((_, index) => (
            <BsStar key={`empty-${index}`} />
          ))}
        </>
      );
    };
  
    return (
        <div className="commentContainer">
        <h4 className="headerStyle">Reviews</h4>
        {/* Comments list */}
        {comments.map((c, index) => (
          <div key={c.reviewId || index} className="commentStyle">
            <strong className="userNameStyle">{c.userName}</strong>
            <div className="ratingStyle">
              {[...Array(5)].map((_, i) => (
                <span key={i} className={`star ${i < c.rating ? "filled" : "empty"}`}>
                  {i < c.rating ? '★' : '☆'}
                </span>
              ))}
            </div>
            <p className="commentTextStyle">{c.comment}</p>
            {index !== comments.length - 1 && <hr className="dividerStyle" />} 
          </div>
        ))}
      </div>
    );
  };
  
  export default CommentsSection;
