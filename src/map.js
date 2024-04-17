import React, { useState, useEffect } from 'react';
import Iframe from 'react-iframe';

const MapView = () => {
  const [address, setAddress] = useState('');

  useEffect(() => {
    fetchAddress();
  }, []);

  const fetchAddress = () => {
    fetch('http://localhost:${5001}', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ address: '' }),
    })
      .then((response) => response.json())
      .then((data) => {
        setAddress(data.address);
      })
      .catch((error) => {
        console.error('Error fetching address:', error);
      });
  };

  return (
    <div className="map-view">
      <Iframe
        url="http://localhost:${5001}"
        width="100%"
        height="100%"
        id="myId"
        className="myClassname"
        display="initial"
        position="relative"
      />
      <p>Address: {address}</p>
      <button onClick={fetchAddress}>Run Algorithm</button>
    </div>
  );
};

export default MapView;