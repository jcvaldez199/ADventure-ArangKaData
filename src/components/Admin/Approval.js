import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Tabs, Tab, Row, Col, Container, Accordion, Card, Table, Navbar } from 'react-bootstrap'
import ReactPlayer from "react-player";
import './TextArea.css'

// Move these to a config file
const reqUrl = "http://localhost:3000/approval/"
const vidDisplayUrl = "http://localhost:3000/video_api/display/"

function Approval() {
  const [req, setReq] = useState(null);

  useEffect(() => {
    axios
      .get(reqUrl,
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
        <Container fluid>

          <Navbar bg="light" expand="lg">
              <Navbar.Brand>Admin page</Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
          </Navbar>

          <Tabs 
            defaultActiveKey="pending" 
            id="uncontrolled-tab-example" 
            className="mb-3"
          >
            <Tab eventKey="pending" title="Pending">
              { !(req == null) &&
                req.filter(items => !items.approved).map(item => (
                <RequestShowBody req={item}/>
                ))}
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

  const reqUrl = 'http://localhost:3000/approval/update';
  const [decision, setDecision] = useState(null);
  function postRequest(event) {
    event.preventDefault()
    axios
      .post(reqUrl, 
        {
          req_id: event.target.elements.formReqid[0].value, 
          decision: decision,
          remarks: event.target.elements.formRemarks.value
        },
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
      )
      .then((response) => {
        console.log(response.data)
        window.location.reload()
      }).catch(error => {
        console.log(error);
      });
  }

  return(
    <form onSubmit={postRequest}>
      <Table striped bordered hover>
        <tbody id="formReqid" value={props.item.id}>
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
            <td>
              <textarea id="formRemarks" className="cell-fill">
                  {props.item.remarks}
              </textarea>
            </td>
          </tr>
        </tbody>
      </Table>
      <Row>
        <Col>
          <Button name="formReqid" onClick={()=>{setDecision(true)}} value={props.item.id} type="submit">Accept</Button>
        </Col>
        <Col>
          <Button name="formReqid" onClick={()=>{setDecision(false)}} value={props.item.id} type="submit">Reject</Button>
        </Col>
      </Row>
    </form>
  );
}

export default Approval;
