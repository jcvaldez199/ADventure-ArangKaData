import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Fade, Button, Form, Tabs, Tab, Row, Col, Container, Accordion, Card, Table } from 'react-bootstrap'
import ReactPlayer from "react-player";
import SendForm from './SendForm'
import { RequestSendUrl, RequestUrlBase, RequestEditUrl, VideoDisplayUrl } from '../config'

function Request() {
  const [req, setReq] = useState(null);

  useEffect(() => {
    axios
      .get(RequestUrlBase,
          { headers: 
            { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
      .then((response) => {
        setReq(response.data);
      }).catch(error => {
        console.log(req);
        setReq(null);
      });
  }, []);

  if (!req) return null;

  return (
    <div>
    <Fade appear={true} in={true}>
    <div>
      <Container fluid>
        <Tabs 
          defaultActiveKey="pending" 
          id="uncontrolled-tab-example" 
          className="mb-3"
        >
          <Tab eventKey="pending" title="Pending">
            { !(req == null) &&
              req.filter(items => !items.approved).map(item => (
              <RequestShowBody req={item} accepted={false}/>
              ))}
          </Tab>
          <Tab eventKey="accepted" title="Accepted">
            { !(req == null) &&
              req.filter(items => items.approved).map(item => (
              <RequestShowBody req={item} accepted={true}/>
              ))}
          </Tab>
          <Tab eventKey="create_new" title="New Request">
            <SendForm />
          </Tab>
        </Tabs>
      </Container>
    </div>
    </Fade>
    </div>
  );
};

function RequestShowBody(props) {
  // should wrap ReactPlayer on a backend request wrapper
  return(
    <Accordion>
      <Card>
        <Accordion.Toggle as={Card.Header} eventKey="0">
          Request id : {props.req.id}
        </Accordion.Toggle>
        <Accordion.Collapse eventKey="0">
          <Card.Body>
            <Row>
              <Col>
                <RequestDescription item={props.req} accepted={props.accepted}/>
              </Col>
              <Col>
                <ReactPlayer url={VideoDisplayUrl.concat(props.req.videoname)} width="100%" height="100%" controls={true} />
              </Col>
            </Row>
          </Card.Body>
        </Accordion.Collapse>
      </Card>
    </Accordion>
  );
}

function RequestDescription(props) {

    const [routes, setRoute] = useState([{}]);
    const [videos, setVideo] = useState([]);
    const [selectedRoute, setSelectedRoute] = useState(props.item.routename);
    const [selectedLocation, setSelectedLocation] = useState(props.item.locname);
    const [selectedVideo, setSelectedVideo] = useState(props.item.videoname);
    const initialRoute = props.item.routename;
    const initialLocation = props.item.locname;
    const initialVideo = props.item.videoname;

    useEffect(() => {
      axios
        .get(RequestSendUrl,
          { headers: 
            { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
        .then((response) => {
          setRoute(response.data[0]);
          setVideo(response.data[1]);
        }).catch(error => {
          setRoute([{}]);
          setVideo([]);
        });
    }, []);

    function handleedit(event) {
      event.preventDefault()
      axios.post(RequestEditUrl.concat(props.item.id), 
        {
          video: event.target.elements.formVideos.value,
          location: event.target.elements.formLocation.value,
          route: event.target.elements.formRoute.value
        },
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
      )
        .then((response) => {
          window.location.reload();
        });
    }
    return(
      <div>
        <Form onSubmit={handleedit}>
              <Table striped bordered hover>
                <tbody>
                  <tr>
                    <td>Last Update</td>
                    <td>{props.item.date_created}</td>
                  </tr>
                  <tr>
                    <td>Last Admin check</td>
                    <td>{props.item.date_decision}</td>
                  </tr>
                  <tr>
                    <td>Route</td>
                    <td>
                      <Form.Group as={Row} controlId="formRoute">
                        <Col sm={10}>
                          <Form.Control 
                            as="select" 
                            onChange={(event) => {setSelectedRoute(event.target.value);
                                                  if (event.target.value === initialRoute) {
                                                    setSelectedLocation(initialLocation);
                                                  }
                                                 }
                                      }
                            value={selectedRoute}
                            disabled={props.accepted}
                          >
                              {Object.keys(routes).map(item => (
                                  <option>{item}</option>
                              ))}
                          </Form.Control>
                        </Col>
                      </Form.Group>
                    </td>
                  </tr>
                  <tr>
                    <td>Location</td>
                    <td>
                      <Form.Group as={Row} controlId="formLocation">
                        <Col sm={10}>
                          <Form.Control as="select" 
                            value={selectedLocation}
                            onChange={(event) => setSelectedLocation(event.target.value)}
                            disabled={props.accepted}
                          >
                            {Object.entries(routes).filter(([key,value]) => key == selectedRoute).map(([key,value]) => (
                              value.map(location => (<option>{location.locname}</option>))
                              ))}
                          </Form.Control>
                        </Col>
                      </Form.Group>
                    </td>
                  </tr>
                  <tr>
                    <td>Video Filename</td>
                    <td>
                      <Form.Group as={Row} controlId="formVideos">
                        <Col sm={10}>
                           <Form.Control as="select" 
                             value={selectedVideo}
                             onChange={(event) => setSelectedVideo(event.target.value)}
                             disabled={props.accepted}
                           >
                              { !(videos == null) &&
                                videos.map(item => (
                                  <option>{item.filename}</option>
                                ))}
                          </Form.Control>
                        </Col>
                      </Form.Group>
                    </td>
                  </tr>
                  <tr>
                    <td>Play counter</td>
                    <td>{props.item.play_counter}</td>
                  </tr>
                  <tr>
                    <td>Remarks</td>
                    <td>{props.item.remarks}</td>
                  </tr>
                </tbody>
              </Table>
          { !(props.accepted) &&
            (
              <Form.Group as={Row}>
                <Col sm={{ span: 10, offset: 2 }}>
                  <Button 
                  type="submit"
                    disabled={ ( initialRoute === selectedRoute && initialLocation === selectedLocation  && initialVideo === selectedVideo ) }
                  >
                    Save Changes
                  </Button>
                </Col>
              </Form.Group>
            )
          }
        </Form>
      </div>
    );
}

export default Request;
