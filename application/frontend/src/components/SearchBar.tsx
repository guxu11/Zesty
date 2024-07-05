import React, { useState } from "react";
import { Alert, InputGroup, FormControl, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom"; 
import "../styles/SearchBar.css";

const SearchBar: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const navigate = useNavigate(); 

  const onSearch = () => {
    if (!searchTerm.trim()) {
      setShowAlert(true);
      setTimeout(() => setShowAlert(false), 1000);
      return;
    }
    navigate(`/search?q=${searchTerm}`);
  };

  return (
    <div className="search-bar-container col-12" style={{ position: "relative" }}>
      <InputGroup>
        <FormControl
          placeholder="Search recipes"
          aria-label="Search recipes"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={(event) => event.key === "Enter" && onSearch()}
        />
        <Button variant="outline-secondary" onClick={onSearch}>Search</Button>
      </InputGroup>
      {showAlert && (
        <Alert variant="danger" style={{ position: "absolute", top: "100%", left: 0, zIndex: 5, width: "100%" }}>
          Please enter a search term.
        </Alert>
      )}
    </div>
  );
};

export default SearchBar;
