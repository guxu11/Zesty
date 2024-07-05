import React from "react";
import { Container, Row, Col } from "react-bootstrap";

import {
  AiFillGithub,
  AiOutlineTwitter,
  AiFillInstagram,
} from "react-icons/ai";
import { FaLinkedinIn } from "react-icons/fa";
import { MdEmail } from "react-icons/md"; // Import Gmail icon
import { FaMusic, FaPaintBrush, FaBrain } from "react-icons/fa";
import "../../styles/about.css";
import Typewriter, { Options } from "typewriter-effect";

export default function RaymondL() {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>
          <Col md={12} className="home-about-description">
            {/* <h1 style={{ fontSize: "2.6em" }}>
              Hello! I am <span className="purple"> Ruxue</span>
            </h1> */}

            <div>
              <Typewriter
                options={{
                  cursor: '<span style="font-size: 2.6rem;">|</span>', // Set cursor size
                  // typeSpeed: 50, // Set typing speed (in milliseconds per character)
                }}
                onInit={(typewriter) => {
                  typewriter

                    .typeString(
                      // 'Hello everyone! I am <span style="color: #b562d6;  font-size: 2.6em;">Ruxue</span> 👋'
                      '<span style="font-size: 2.6em;">Hello everyone! I am <span style="color: #ff7f50;">Raymond</span> 👋</span>'
                    )
                    // .pauseFor(10)
                    .start();
                }}
              />
            </div>

            <p className="home-about-body">
              I am an undergraduate student majoring{" "}
              <i>
                <b className="purple">Computer Science. </b>
              </i>
              <br />
              <br />
              I am fluent in classics like{" "}
              <i>
                <b className="purple">C++ and Java. </b>
              </i>
              <br />
              <br />
              My field of Interest's are learning new &nbsp;
              <i>
                <b className="purple">Salesforce Development </b> and
                also {" "}
                <i>
                  <b className="purple">Unreal Engine.</b> 
                </i>
              </i>
              <br />
              <br />
              In my spare time, I enjoy playing video games, watching movie, hanging out, and
              working out.
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
                  href="https://github.com/Airray117"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
             
              <li className="social-icons">
                <a
                  href="https://www.linkedin.com/in/raymond-liu-2b7b4a196/"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour home-social-icons"
                >
                  <FaLinkedinIn />
                </a>
              </li>
            </ul>
          </Col>
        </Row>
      </Container>
    </Container>
  );
}
