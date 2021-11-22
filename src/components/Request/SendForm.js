import React, { useEffect, useState } from 'react'
import { Button, Form, Row, Col } from 'react-bootstrap'
import axios from 'axios'
import { RequestSendUrl } from '../config'
import { RouteUrlBase } from '../config'
import { MapContainer, TileLayer, FeatureGroup , CircleMarker, Circle, useMap, setView } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';


function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

function SendForm() {

  const [routes, setRoute] = useState([{}]);
  const [videos, setVideo] = useState([]);
  const [selectedRoute, setSelect] = useState("");
  const [map, setMap] = useState(() => (<div className="App">Loading Map...</div>));
  const [center, setCenter] = useState([]);
  const [points, setPoints] = useState([[]]);

  const redOptions = { color : 'red' };
  const blueOptions = { color : 'blue' };
  const [currColor, setColor] = useState({ color : 'red' });
  const [currBorder, setBorder] = useState([]);

  const [newLoc, setNewLoc] = useState(true);
  const [modeSwitchNewLoc, setModeSwitch] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState(null);


  if (currBorder.length > 1 || modeSwitchNewLoc) {
    setMap(retrieveMapDetails(selectedRoute));
    setBorder([]);
    setModeSwitch(false);
  }

  function renderMap(gpspoints){
    return (
       <div>
         <MapContainer center={gpspoints[Math.floor(gpspoints.length/2)]} zoom={13} scrollWheelZoom={false} style={{ height: '100vh', width: '100wh' }}>
           <ChangeView center={gpspoints[Math.floor(gpspoints.length/2)]} zoom={13} /> 
           <TileLayer
             attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
             url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
           />
           { gpspoints.map((item, index) => (
             (selectedLocation) ? 
               <Circle 
                 center={item}
                 pathOptions={(index >= currBorder[0] && index <= currBorder[1]) ? blueOptions : redOptions}
                 radius={2} />
             :
               <CircleMarker 
                 center={item}
                 pathOptions={(index >= currBorder[0] && index <= currBorder[1]) ? blueOptions : redOptions}
                 eventHandlers={{
                     click: (e) => {
                       setBorder(oldArray => (oldArray[0] > index) ? [index, ...oldArray] : [...oldArray, index]);
                     },
                 }}
               radius={2} />
           ))}
         </MapContainer>
       </div>
    );
  }

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
    axios.get(`${RouteUrlBase}/${routename}`,
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
      .then((response) => {
        setPoints(response.data);
        setCenter(response.data[0] );
        setMap(renderMap(response.data, null));
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
                        setBorder([]);
                        setModeSwitch(true);
                        setSelectedLocation(null);
                        setNewLoc(true);
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
              { (!newLoc) ?
                <Form.Control as="select" 
                onChange={(e)=>{
                    let tempBorder = Object.entries(routes)
                      .filter(([key,value]) => key == selectedRoute)
                      .map(([key,value]) => value
                      .filter(loc => loc.locname == e.target.value)
                      .map(loc => [loc.startindex,loc.lastindex])
                    )[0][0];
                    setBorder(tempBorder);
                    setSelectedLocation(e.target.value);
                  }}>
                  {Object.entries(routes).filter(([key,value]) => key == selectedRoute).map(([key,value]) => (
                    value.map(location => (<option>{location.locname}</option>))
                  ))}
                </Form.Control>
                :
                <Form.Control type="text"></Form.Control>
              }
            </Col>
            <Col>
              <Button onClick={() => {
                if (!newLoc) {
                  // this means state will be set to drawing a new location
                  setBorder([]);
                  setModeSwitch(true);
                  setSelectedLocation(null);
                } else {
                  let tempBorder = Object.entries(routes)
                    .filter(([key,value]) => key == selectedRoute)
                    .map(([key,value]) => value.map(loc => [loc.startindex,loc.lastindex, loc.locname])
                  )[0][0];
                  setBorder(tempBorder.slice(0,2));
                  setSelectedLocation(tempBorder[2]);
                }
                setNewLoc(oldstate => (!oldstate));
                }}
              >
                {(!newLoc) ? "Add New" : "Use Existing"}
              </Button>
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
