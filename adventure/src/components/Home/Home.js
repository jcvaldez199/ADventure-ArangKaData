import React from 'react'
import { Fade } from 'react-bootstrap'

export const Home = () => (
    <div class="center">
      <Fade appear={true} in={true}>
        <div>
            <h2> Welcome to ADventure </h2>
            <h5> Click on the Navigation Tabs to get started. </h5>
        </div>
      </Fade>
    </div>
);

