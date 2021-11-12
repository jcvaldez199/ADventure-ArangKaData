import React, { useEffect, useState } from 'react'
import { Button, Form, Row, Col } from 'react-bootstrap'
import axios from 'axios'
import { MapContainer, TileLayer, Circle } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';


function MyMap() {

  const redOptions = { color : 'red' }
  const center = [51.505, -0.09]

  return (
    <div>
    <MapContainer center={center} zoom={13} scrollWheelZoom={false} style={{ height: '100vh', width: '100wh' }}>
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Circle center={center} pathOptions={redOptions} radius={1} />
    </MapContainer>
    </div>
  );
};


export default MyMap;
