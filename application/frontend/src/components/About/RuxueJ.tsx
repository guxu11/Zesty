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

export default function RuxueJ() {
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
                      '<span style="font-size: 2.6em;">Hello everyone! I am <span style="color: #fe9438;">Ruxue</span> 👋</span>'
                    )
                    // .pauseFor(10)
                    .start();
                }}
              />
            </div>

            <p className="home-about-body">
              I am a master student majoring{" "}
              <i>
                <b className="purple">Computer Science. </b>
              </i>
              <br />
              <br />
              My bachelor degree is{" "}
              <i>
                <b className="purple">Civil Engineering. </b>
              </i>
              <br />
              <br />
              My field of Interest's are learning new &nbsp;
              <i>
                <b className="purple">Web Technologies and Products </b> and
                also in areas related to{" "}
                <i>
                  <b className="purple">Music</b> <FaMusic /> Art and{" "}
                  <FaPaintBrush /> Psychology <FaBrain />.{" "}
                </i>
              </i>
              <br />
              <br />
              In my spare time, I enjoy playing music, watching movie and
              cleaning the room.
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
                  href="https://github.com/RuxueJ"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
              <li className="social-icons">
                <a
                  href="mailto:rjin@sfsu.edu"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour home-social-icons"
                >
                  <MdEmail />
                </a>
              </li>
              <li className="social-icons">
                <a
                  href="https://www.linkedin.com/in/ruxue-jin/"
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
