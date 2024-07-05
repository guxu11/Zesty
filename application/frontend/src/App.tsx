import About from "./components/About/About";
import RuxueJ from "./components/About/RuxueJ";
import XuG from "./components/About/XuG";
import PasangS from "./components/About/PasangS";
import DanteV from "./components/About/DanteV";
import Youtheezus from "./components/About/yontheezus";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/Home/Home";
import "./App.css";
import React from "react";
import JunghyunS from "./components/About/JunghyunS";
import RaymondL from "./components/About/RaymondL";

import RecipeDetailMissingIngredientsPage from "./components/Recipe/RecipeDetailMissingIngredients";
import RecipeDetailPage from "./components/Recipe/RecipeDetail";
import NavigationBar from "./components/NavigationBar";
import RegisterPage from "./components/Register";
import Login from "./components/Login";
import { AuthProvider } from "./components/Context/AuthContext";
import SearchResults from "./components/Home/SearchResults";
import CreateRecipePage from "./components/Recipe/CreateRecipe";
import Profile from "./components/Profile/Profile";
import GetPantryRecipes from "./components/Home/GetPantryRecipe";

function App() {
  // React.useEffect(() => {
  //   document.body.classList.add("dark-theme");

  //   return () => {
  //     document.body.classList.remove("dark-theme");
  //   };
  // }, []);
  return (
    <AuthProvider>
      <Router>
        <div>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<SearchResults />} />
            <Route path="/about" element={<About />} />
            <Route path="/about/RuxueJ" element={<RuxueJ />} />
            <Route path="/about/XuG" element={<XuG />} />
            <Route path="/about/JunghyunS" element={<JunghyunS />} />
            <Route path="/about/PasangS" element={<PasangS />} />
            <Route path="/about/DanteV" element={<DanteV />} />
            <Route path="/about/RaymondL" element={<RaymondL />} />
            <Route path="/about/YonatanL" element={<Youtheezus />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<Login />} />

            <Route path="/recipe/:recipeId" element={<RecipeDetailPage />} />
            <Route path="/recipe/missing/:recipeId" element={<RecipeDetailMissingIngredientsPage />} />
            <Route path="/create-recipe" element={<CreateRecipePage />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/pantry-recipes" element={<GetPantryRecipes />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
