import React from 'react';
import './App.css';
import MapView from './map';

class RightSideWidget extends React.Component {
  render() {
    return (
      <div className="right-side-widget">
        <MapView />
      </div>
    );
  }
}

export default RightSideWidget;