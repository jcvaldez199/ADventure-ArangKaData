import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Form, Tabs, Tab, Row, Col, Container, Accordion, Card, Table } from 'react-bootstrap'
import ReactPlayer from "react-player";
import SendForm from './SendForm'

// Move these to a config file
const reqUrl = "http://localhost:3000/request_api/"
const reqSendUrl = "http://localhost:3000/request_api/send"
const vidDisplayUrl = "http://localhost:3000/video_api/display/"

function Request() {
  const [req, setReq] = useState([{}]);

  useEffect(() => {
    axios.get(reqUrl).then((response) => {
      setReq(response.data);
    });
  }, []);

  if (!req) return null;

  return (
    <div>
      <Container fluid>
        <Tabs 
          defaultActiveKey="pending" 
          id="uncontrolled-tab-example" 
          className="mb-3"
        >
          <Tab eventKey="pending" title="Pending">
            {req.filter(items => !items.approved).map(item => (
              <RequestShowBody req={item}/>
              ))}
          </Tab>
          <Tab eventKey="accepted" title="Accepted">
            {req.filter(items => items.approved).map(item => (
              <RequestShowBody req={item}/>
              ))}
          </Tab>
          <Tab eventKey="create_new" title="New Request">
            <SendForm />
          </Tab>
        </Tabs>
      </Container>
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
                <RequestDescription item={props.req}/>
              </Col>
              <Col>
                <ReactPlayer url={vidDisplayUrl.concat(props.req.videoname)} width="100%" height="100%" controls={true} />
              </Col>
            </Row>
          </Card.Body>
        </Accordion.Collapse>
      </Card>
    </Accordion>
  );
}

function RequestDescription(props) {
    return(
        <Table striped bordered hover>
          <tbody>
            <tr>
              <td>Date created</td>
              <td>{props.item.date_created}</td>
            </tr>
            <tr>
              <td>Last Admin check</td>
              <td>{props.item.date_decision}</td>
            </tr>
            <tr>
              <td>Route</td>
              <td>{props.item.routename}</td>
            </tr>
            <tr>
              <td>Location</td>
              <td>{props.item.locname}</td>
            </tr>
            <tr>
              <td>Video Filename</td>
              <td>{props.item.videoname}</td>
            </tr>
            <tr>
              <td>Remarks</td>
              <td>{props.item.remarks}</td>
            </tr>
          </tbody>
        </Table>
    );
}

export default Request;
