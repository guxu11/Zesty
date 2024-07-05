import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import myImg from "../../assets/team-01.png";

import {
  AiFillGithub,
  AiFillInstagram,
} from "react-icons/ai";
import { FaLinkedinIn } from "react-icons/fa";
import "../../styles/about.css";
import Typewriter, { Options } from "typewriter-effect";


export default function JunghyunS() {
  // const App: React.FC = () => {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>
          <Col md={12} className="home-about-description">
            <h1 style={{ fontSize: "2.6em" }}>
              Hi everyone, I am <span className="purple"> Katie</span>
            </h1>
            <Typewriter
              options={{
                strings: ["Hi, I'm Junghyun! Please call me Katie😆"],
                autoStart: true,
                loop: true,
                deleteSpeed: 0,
              }}
            />
            {/* <ReactTyped strings={["My React App"]} typeSpeed={100} loop /> */}
            <p className="home-about-body">
              I'm an exchange student from South Korea. I'm a junior in Computer Science.
              <br />
              <br />I am fluent in classics like
              <i>
                <b className="purple"> C++ and Python. </b>
              </i>
              <br />
              <br />
              My field of Interest's are building new
              <i>
                <b className="purple"> Web Technologies and Products. </b> 
              </i>
              <br />
              <br />
              I'm also interested in 
              <i>
                <b className="purple"> Project Managing, </b>
              </i>
              so I hope to experience many team projects like <b className="purple"> Hackathons.</b>
              <br />
              <br />
              Now I'm applying my passion for learning
              <i>
                <b className="purple"> React.js.</b>
              </i>
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
                  href="https://github.com/katie424"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
              <li className="social-icons">
                <a
                  href="https://www.instagram.com/j_hyuuun2"
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
