import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import myImg from "../../assets/team-01.png";
import daisyImage from "../../assets/Daisy.jpg";

import {
  AiFillGithub,
  AiOutlineTwitter,
  AiFillInstagram,
} from "react-icons/ai";
import { FaLinkedinIn } from "react-icons/fa";
import "../../styles/about.css";
import Typewriter, { Options } from "typewriter-effect";


export default function DanteV() {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>
          <Col md={12} className="home-about-description">
            <h1 style={{ fontSize: "2.6em" }}>
              Hello! I am <span className="purple"> Dante</span>
            </h1>
            <Typewriter
              options={{
                strings: ["Hello I am Dante"],
                autoStart: true,
                loop: true,
                deleteSpeed: 0,
              }}
            />
            {/* <ReactTyped strings={["My React App"]} typeSpeed={100} loop /> */}
            <p className="home-about-body">
              I'm a undergraduate student at San Francisco State University!
              <br />
              <br />I am fluent in
              <i>
                <b className="purple"> C++, Java and Python. </b>
              </i>
              <br />
              <br />
              My field of Interest is &nbsp;
              <i>
                <b className="purple">Machine Learning </b>
              </i>
              <br />
              <br />
              I also love cats, especially my cat Daisy!
            </p>
            <Col md={3} className="myAvtar">
              <img src={daisyImage} className="img-fluid" alt="daisy" />
          </Col>
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
                  href="https://github.com/Dantejv"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
            </ul>
          </Col>
        </Row>
      </Container>
    </Container>
  );
}
