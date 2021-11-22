import React, { useEffect, useState } from 'react'
import { Button, Form, Row, Col } from 'react-bootstrap'
import axios from 'axios'
import { MapContainer, TileLayer, Circle } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';
import { RouteUrlBase } from '../config'


function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

function MyMap(props) {

  const redOptions = { color : 'red' };
  const defMap = props.defaultMap;
  const [center, setCenter] = useState([]);
  const [points, setPoints] = useState([[]]);
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${RouteUrlBase}/${defMap}`,
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
      .then((response) => {
        setPoints(response.data);
        setCenter( response.data[0] );
        console.log(response.data[0]);
        setLoading(false);
      }).catch(error => {
        setPoints([[]]);
        setCenter([]);
      });
  }, []);
  
  if (isLoading) {
    return <div className="App">Loading Map...</div>;
  }

  return (
    <div>
    <MapContainer center={center} zoom={13} scrollWheelZoom={false} style={{ height: '100vh', width: '100wh' }}>
      <ChangeView center={center} zoom={zoom} />
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      { !(points == null) &&
        points.map(item => (
        <Circle center={item} pathOptions={redOptions} radius={1} />
      ))}
    </MapContainer>
    </div>
  );
};


export ChangeView;
export MyMap;
