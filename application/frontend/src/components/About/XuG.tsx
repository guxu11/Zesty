import React from "react";
import { Container, Row, Col } from "react-bootstrap";

import {
  AiOutlineMail,
  AiFillGithub,
} from "react-icons/ai";

import { FaLinkedinIn } from "react-icons/fa";
import "../../styles/about.css";
import styles from "../../styles/xu_page.module.css";
import Typewriter, { Options } from "typewriter-effect";
import avatar from "../../assets/xugu_avatar.png";

export default function XuG() {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>

        <Col md={12} className="home-about-description"> 
        <div className={styles.Typewriter__wrapper}>
            <Typewriter
              onInit={(typewriter) => {
                typewriter
                  .typeString('Hi there! I am <span style="color: #ff7f50; ">Xu Gu</span> 👋')
                  .start();
              }}
            />
          </div>
        </Col>
          <Col md={8} className="home-about-description">
       
          <h2 style={{ fontSize: "1.6em" }}>
              ABOUT ME
            </h2>

            <p className="home-about-body">
              I'm a graduate student at San Francisco State University pursuing Master's degree in Computer Science.
              <br />
              <br />I am fluent in classics like
              <i>
                <span className={styles.p_xu}> Java, Python and C++. </span>
              </i>
              <br />
              <br />
              My field of Interest's are building new &nbsp;
              <i>
                <b className="purple">Web Technologies and Products </b> and
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
          <Col md={4} className="myAvtar">
              <img src={avatar} className="img-fluid" alt="avatar" />
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
                  href="https://github.com/guxu11"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
              <li className="social-icons">
                <a
                  href="https://www.linkedin.com/in/xu-gu-a5177b1b0"
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
