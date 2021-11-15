import React from 'react'
import { MapContainer, TileLayer, Circle, useMap, setView } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';

function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

function MyMap(props) {

  const redOptions = { color : 'red' };

  return (
    <div>
    <MapContainer center={props.center} zoom={13} scrollWheelZoom={false} style={{ height: '100vh', width: '100wh' }}>
      {props.changeView}
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      { props.points.map(item => (<Circle center={item} pathOptions={redOptions} radius={1} />)) }
    </MapContainer>
    </div>
  );
};


export default MyMap;
