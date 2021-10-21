import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Form, Row, Col, Container, Tooltip, Card, CardDeck, OverlayTrigger } from 'react-bootstrap'
import ReactPlayer from "react-player";
import { VideoUrlBase, VideoPostUrl, VideoDisplayUrl } from '../config'

function Video() {
  const [vid, setVid] = useState(null);
  const [currentVid, setCurrent] = useState(null);

  useEffect(() => {
    axios
      .get(VideoUrlBase, 
          { headers: 
            { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
      .then((response) => {
        setVid(response.data);
        setCurrent(response.data[0]);
      })
      .catch(error => {
        setVid(null);
        setCurrent(null);
    });
  }, []);

  function postVid(event) {
    event.preventDefault()
    console.log(event.target.elements.vidfile.files[0])
    var formData = new FormData();
    formData.append("file", event.target.elements.vidfile.files[0]);
    axios
      .post(VideoPostUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then((response) => {
      setCurrent(response.data);
      setVid(prevState => ([...prevState,response.data]));
    });
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
              { !(vid == null) &&
                vid.map(item => (
                <Card>
                  <Card.Img variant="bottom" src={VideoDisplayUrl.concat(item.thumbnail)} />
                  <Card.Body>
                    <Card.Text>
                      <OverlayTrigger
                        placement="top"
                        delay={{ show: 250, hide: 400 }}
                        overlay={renderTooltip}
                      >
                        <Button value={item} onClick={() => setCurrent(item)}>{item.filename}</Button>
                      </OverlayTrigger>
                    </Card.Text>
                  </Card.Body>
                </Card>
              ))}
              <Card>
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
            { !(currentVid == null) &&
            <ReactPlayer url={VideoDisplayUrl.concat(currentVid.filename)} width="100%" height="100%" controls={true} />
            }
          </Col>
        </Row>
      </Container>
    </div>
  );
};


export default Video;

