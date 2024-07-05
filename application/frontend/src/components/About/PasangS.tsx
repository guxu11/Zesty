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


export default function PasangS() {
  // const App: React.FC = () => {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>
          <Col md={12} className="home-about-description">
            <h1 style={{ fontSize: "2.6em" }}>
              Hello! I am <span className="purple"> Pasang</span>
            </h1>
            <Typewriter
              options={{
                strings: ["Hello I am Pasang Sherpa"],
                autoStart: true,
                loop: true,
                deleteSpeed: 0,
              }}
            />
            {/* <ReactTyped strings={["My React App"]} typeSpeed={100} loop /> */}
            <p className="home-about-body">
              I am an undergrad Com Sci student at SF State. I'll be graduating some time in 2024.
              <br />
              <br />I am fluent in classics like
              <i>
                <b className="purple"> C++, Javascript and some C. </b>
              </i>
              <br />
              <br />
              My field of Interest is &nbsp;
              <i>
                <b className="purple">Cyber Security </b> and
                also in areas related to <b className="purple">Blockchain.</b>
              </i>
              <br />
              <br />
              Whenever possible, I also apply my passion for developing products
              with <b className="purple">Node.js</b> and
              <i>
                <b className="purple">
                  {" "}
                  Modern Javascript Library and Frameworks
                </b>
              </i>
              &nbsp; like
              <i>
                <b className="purple"> React.js and Next.js</b>
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
                  href="https://github.com/TimedT"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
              <li className="social-icons">
                <a
                  href="https://www.linkedin.com/in/pasang-sherpa-1b1b61250/"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
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
