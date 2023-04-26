<template>
  <div>
    <div class="row">
      <h2>About</h2>
      <p>
        This web application is running on an AWS EC2 in multiple docker
        containers. The purpose of this application is to demonstrate fishing
        areas being defined by spatial objects (polygons, lines, ect...). It
        also demonstrates using GeoJSON as a transfer medium for these spatial
        objects, both for transfering objects from major GIS applications into a
        database over the internet as well as front-ends communication with
        back-ends to display maps.
      </p>
    </div>
    <div class="row">
      <h2>Stack</h2>

      <div class="column">
        <h3>Front-end</h3>
        <ul>
          <li><a href="https://vuejs.org/">VueJS</a></li>
          <li><a href="https://leafletjs.com/">LeafletJS</a></li>
        </ul>
      </div>
      <div class="column">
        <h3>Back-end</h3>
        <ul>
          <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
          <li><a href="https://www.sqlalchemy.org/">SQLAlchemy</a></li>
          <li><a href="https://www.postgresql.org/">PostgreSQL</a></li>
          <li><a href="https://postgis.net/">PostGIS</a></li>
        </ul>
      </div>
      <div class="column">
        <h3>Server-side</h3>
        <ul>
          <li><a href="https://aws.amazon.com/">Amazon Web Services</a></li>
          <li><a href="https://www.docker.com/">Docker</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style>
.column {
  float: left;
  width: 33.33%;
}

/* Clear floats after the columns */
.row:after {
  margin-top: 30px;
  content: "";
  display: table;
  clear: both;
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
}
</style>
