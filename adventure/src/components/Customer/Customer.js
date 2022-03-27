import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Fade, Button, Form, Row, Col, Container, Card, Table } from 'react-bootstrap'
import { CustomerMetricsUrl } from '../config'

export const Customer = () => (
    <div class="center">
      <Fade appear={true} in={true}>
        <div>
          <Container fluid>
            <Row>
              <Col>
                <ProfileBody />
              </Col>
            </Row>
          </Container>
        </div>
      </Fade>
    </div>
);

function ProfileBody(props) {

  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    axios
      .get(CustomerMetricsUrl,
          { headers: 
            { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
      .then((response) => {
        setMetrics(response.data[0]);
        console.log(response.data[0])
      }).catch(error => {
        setMetrics(null);
      });
  }, []);

  return(
    <Card>
      <Card.Header as="h5"> User : {metrics ? metrics.username : "Unavailable"}</Card.Header>
        <Card.Body>
          <Table striped bordered hover>
            <tbody>
              <tr>
                <td>Total Requests</td>
                <td>{metrics ? metrics.request_count : "Unavailable"}</td>
              </tr>
              <tr>
                <td>Overall Video Playcount</td>
                <td>{metrics ? metrics.vid_count_total : "Unavailable"}</td>
              </tr>
            </tbody>
          </Table>
        </Card.Body>
    </Card>
  );
}
