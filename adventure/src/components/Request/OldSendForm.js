import React, { useEffect, useState } from 'react'
import { Button, Form, Row, Col } from 'react-bootstrap'
import axios from 'axios'
import { RequestSendUrl } from '../config'
import { RouteUrlBase } from '../config'
import { MapContainer, TileLayer, FeatureGroup , Circle, useMap, setView } from 'react-leaflet'
import { EditControl } from "react-leaflet-draw"
import 'leaflet/dist/leaflet.css';
import "leaflet-draw/dist/leaflet.draw-src.css";


function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

const MapDrawer = () => (
  <FeatureGroup>
    <EditControl
      position='topright'
      onEdited={this._onEditPath}
      onCreated={this._onCreate}
      onDeleted={this._onDeleted}
      draw={{
        rectangle: false
      }}
    />
    <Circle center={[51.51, -0.06]} radius={200} />
  </FeatureGroup>
);

function SendForm() {

  const [routes, setRoute] = useState([{}]);
  const [videos, setVideo] = useState([]);
  const [selectedRoute, setSelect] = useState("");
  const [map, setMap] = useState(() => (<div className="App">Loading Map...</div>));
  const [center, setCenter] = useState([]);
  const [points, setPoints] = useState([[]]);
  const redOptions = { color : 'red' };
        

  useEffect(() => {
    axios
      .get(RequestSendUrl,
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
      .then((response) => {
        setRoute(response.data[0]);
        setVideo(response.data[1]);
        setSelect( Object.keys(response.data[0])[0] );
        retrieveMapDetails(Object.keys(response.data[0])[0]);
      }).catch(error => {
        setRoute([{}]);
        setVideo([]);
      });
  }, []);

  function postRequest(event) {
    event.preventDefault()
    axios.post(RequestSendUrl, 
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

  function retrieveMapDetails(routename) {
    console.log(routename);
    axios.get(`${RouteUrlBase}/${routename}`,
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
      .then((response) => {
        setPoints(response.data);
        setCenter(response.data[0] );
        setMap(() => (
           <div>
             <MapContainer center={response.data[Math.floor(response.data.length/2)]} zoom={13} scrollWheelZoom={false} style={{ height: '100vh', width: '100wh' }}>
               <ChangeView center={response.data[Math.floor(response.data.length/2)]} zoom={13} /> 
               <TileLayer
                 attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                 url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
               />
               { response.data.map(item => (<Circle center={item} pathOptions={redOptions} radius={1} />)) }
             </MapContainer>
           </div>
        ));
      }).catch(error => {
        setPoints([[]]);
        setCenter([]);
      });
  }

  return (
    <div>
    <Row>
     <Col>
        <Form onSubmit={postRequest}>
          <Form.Group as={Row} controlId="formRoute">
            <Form.Label column sm={2}> Route </Form.Label>
            <Col sm={10}>
              <Form.Control 
                as="select" 
                onChange={(event) => {
                        setSelect(event.target.value);
                        retrieveMapDetails(event.target.value);
                }}
                value={selectedRoute}
              >
                  {Object.keys(routes).map(item => (
                      <option>{item}</option>
                  ))}
              </Form.Control>
            </Col>
          </Form.Group>

          <Form.Group as={Row} controlId="formLocation">
            <Form.Label column sm={2}> Location </Form.Label>
            <Col sm={7}>
              <Form.Control as="select">
                {Object.entries(routes).filter(([key,value]) => key == selectedRoute).map(([key,value]) => (
                  value.map(location => (<option>{location.locname}</option>))
                ))}
              </Form.Control>
            </Col>
            <Col>
              <Button>Add New</Button>
            </Col>
          </Form.Group>

          <Form.Group as={Row} controlId="formVideos">
            <Form.Label column sm={2}> Videos </Form.Label>
            <Col sm={10}>
               <Form.Control as="select" defaultValue="Choose...">
                  { !(videos == null) &&
                    videos.map(item => (
                      <option>{item.filename}</option>
                    ))}
              </Form.Control>
            </Col>
          </Form.Group>

          <Form.Group as={Row}>
            <Col sm={{ span: 10, offset: 2 }}>
              <Button type="submit">Send</Button>
            </Col>
          </Form.Group>
        </Form>
     </Col>
     <Col xs={8}>
        <Row>
          <Col>{map}</Col>
        </Row>
     </Col>
    </Row>
    </div>
  );
};


export default SendForm;
