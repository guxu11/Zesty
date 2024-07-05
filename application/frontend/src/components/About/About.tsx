import { Link } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";
import xgu from "../../assets/xgu.jpg";
import ruxue from "../../assets/Ruxue.jpg";
import raymond from "../../assets/Raymond.webp";
import pasang from "../../assets/pasang.jpg";
import katie from "../../assets/Katie.png";
import yonatan from "../../assets/yonatan.jpg";
import dante from "../../assets/Dante.jpg";
import "../../styles/about.css";

const teamMembers = [
  { name: "Xu Gu", route: "XuG", position: "Team Leader", imageUrl: xgu },
  {
    name: "Ruxue Jin",
    route: "RuxueJ",
    position: "Front-end Lead",
    imageUrl: ruxue,
  },
  {
    name: "Yonatan Leake",
    route: "YonatanL",
    position: "Scrum Master",
    imageUrl: yonatan,
  },
  {
    name: "Raymond Liu",
    route: "RaymondL",
    position: "Git Master",
    imageUrl: raymond,
  },
  {
    name: "Pasang Sherpa",
    route: "PasangS",
    position: "Back-end Lead",
    imageUrl: pasang,
  },
  {
    name: "Junghyun Song",
    route: "JunghyunS",
    position: "Front-end Lead",
    imageUrl: katie,
  },
  {
    name: "Dante Vercelli",
    route: "DanteV",
    position: "Back-end Lead",
    imageUrl: dante,
  },
];

export default function About(): JSX.Element {
  return (
    <section className="our__team">
      <div className="container">
        <div className="team__content">
          <h1 style={{ paddingBottom: 15 }} className="heading">
            Hello CSC 648/848{" "}
            <span className="wave" role="img" aria-labelledby="wave">
              👋🏻
            </span>
          </h1>

          <h1 className="heading-name">
            We're
            <strong className="main-name"> Riduculous Team 5</strong>
          </h1>
        </div>
        <Container className="team__wrapper">
          <Row className="justify-content-center">
            {teamMembers.map((member, index) => (
              <Col
                key={index}
                xs={9}
                sm={9}
                md={6}
                lg={4}
                xl={3}
                className="mb-4"
              >
                <Link to={`/about/${member.route}`}>
                  <div className="team__item" key={index}>
                    <div className="team__img">
                      <img src={member.imageUrl} />
                    </div>
                    <div className="team__details">
                      <h3>{member.name}</h3>
                      <h4 className="description">{member.position}</h4>
                    </div>
                  </div>
                </Link>
              </Col>
            ))}
          </Row>
        </Container>
      </div>
    </section>
  );
}
