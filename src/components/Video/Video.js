import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Form, Row, Col, Container, Tooltip, Card, CardDeck, OverlayTrigger } from 'react-bootstrap'
import ReactPlayer from "react-player";

// Move these to a config file
const vidUrl = "http://localhost:3000/video_api/"
const vidPostUrl = "http://localhost:3000/video_api/upload/"
const vidDisplayUrl = "http://localhost:3000/video_api/display/"

function Video() {
  const [vid, setVid] = useState([]);
  const [currentVid, setCurrent] = useState("");

  useEffect(() => {
    axios.get(vidUrl).then((response) => {
      setVid(response.data);
      setCurrent(response.data[0].filename);
    });
  }, []);

  function postVid(event) {
    event.preventDefault()
    console.log(event.target.elements.vidfile.value)
    /*axios.post(reqSendUrl, 
      {
        video: event.target.elements.formVideos.value,
        location: event.target.elements.formLocation.value,
        route: event.target.elements.formRoute.value
      })
      .then((response) => {
        console.log("must redirect");
      });*/
  }

  const renderTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props}>
      Play
    </Tooltip>
  );

  return (
    <div>
      <Container>
        <Row>
          <Col>
            <CardDeck>
              {vid.map(item => (
                <Card>
                  <Card.Img variant="bottom" src="holder.js/100px160" />
                  <Card.Body>
                    <Card.Text>
                      <OverlayTrigger
                        placement="top"
                        delay={{ show: 250, hide: 400 }}
                        overlay={renderTooltip}
                      >
                        <Button value={item} onClick={() => setCurrent(item.filename)}>{item.filename}</Button>
                      </OverlayTrigger>
                    </Card.Text>
                  </Card.Body>
                </Card>
              ))}
              <Card>
                <Card.Img variant="bottom" src="holder.js/100px160" />
                <Card.Body>
                  <Card.Text>
                    <Form onSubmit={postVid}>
                      <Form.Group>
                        <Form.File id="vidfile" label="Upload new Video" />
                      </Form.Group>
                      <Form.Group>
                        <OverlayTrigger
                          placement="right"
                          delay={{ show: 250, hide: 400 }}
                          overlay={renderTooltip}
                        >
                          <Button type="submit">Upload New</Button>
                        </OverlayTrigger>
                      </Form.Group>
                    </Form>
                  </Card.Text>
                </Card.Body>
              </Card>
            </CardDeck>
          </Col>
          <Col>
            <ReactPlayer url={vidDisplayUrl.concat(currentVid)} width="100%" height="100%" controls={true} />
          </Col>
        </Row>
      </Container>
    </div>
  );
};


export default Video;

