import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import myImg from "../../assets/team-01.png";

import {
  AiFillGithub,
  AiOutlineTwitter,
  AiFillInstagram,
} from "react-icons/ai";
import { FaLinkedinIn } from "react-icons/fa";
import "../../styles/about.css";
import Typewriter, { Options } from "typewriter-effect";


export default function RuxueJ() {
  // const App: React.FC = () => {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>
          <Col md={12} className="home-about-description">
            <h1 style={{ fontSize: "2.6em" }}>
              Hello! I am <span className="purple"> Yonatan!!</span>
            </h1>
            <Typewriter
              options={{
                strings: ["Hello I am Yonatan"],
                autoStart: true,
                loop: true,
                deleteSpeed: 0,
              }}
            />
            {/* <ReactTyped strings={["My React App"]} typeSpeed={100} loop /> */}
            <p className="home-about-body">
              I am an undergraduate student looking to finish my degree in Computer Science
              here at San Francisco State University
              <br />
              <br />I am familiar in languages like
              <i>
                <b className="purple"> C++, Javascript and Java. </b>
              </i>
              <br />
              <br />
              Some of my hobbies outside of programming include &nbsp;
              <i>
                <b className="purple">watching sports, hanging out with friends </b> and
                exploring the <b className="purple">Bay Area.</b>
              </i>
              <br />
              <br />
              I started my computer science journey during the pandemic <b className="purple">and</b> hope 
              to find a fruitful career ahead.     
            </p>
          </Col>
        </Row>

        <Row>
          <Col md={12} className="home-about-social">
            <h1>FIND ME ON</h1>
            <p>
              Feel free to <span className="purple">connect </span>with me
            </p>
            <ul className="home-about-social-links">
              <li className="social-icons">
                <a
                  href="https://github.com/yontheezus"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
              <li className="social-icons">
                <a
                  href="https://www.linkedin.com/in/yontheezus/"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <FaLinkedinIn />
                </a>
              </li>
              <li className="social-icons">
                <a
                  href="https://www.instagram.com/yontheezus/"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour home-social-icons"
                >
                  <AiFillInstagram />
                </a>
              </li>
            </ul>
          </Col>
        </Row>
      </Container>
    </Container>
  );
}
