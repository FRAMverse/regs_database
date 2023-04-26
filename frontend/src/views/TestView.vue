<template>
  <div>
    <div id="map"></div>
    <h3>Choose an area to display</h3>
    <select v-model="selected" @change="getGeom()" style="width: 100%">
      <option
        v-for="area in areas"
        :value="area.catch_area_id"
        :key="area.description"
      >
        {{ area.description }}
      </option>
    </select>
    <div>
      <h3>Upload GeoJSON</h3>
      <div>
        <input type="file" @change="uploadFile" ref="file" />
        <input
          type="text"
          v-model="description"
          placeholder="Description of regulation area"
          style="margin-right: 20px; width: 50%"
        />
        <button @click="submitFile">Upload!</button>
      </div>
      <div class="message" v-if="message">
        <span>{{ message }}</span>
      </div>
    </div>
  </div>
</template>
<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";

export default {
  name: "LeafletMap",
  data() {
    return {
      map: null,
      geom: null,
      uploadGeom: null,
      selected: null,
      areas: [],
      message: null,
      description: null,
    };
  },
  mounted() {
    this.map = L.map("map").setView([47.6, -122.335], 6);
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.map);
    this.axios.get("http://127.0.0.1:8000/api/catchareas/").then((response) => {
      this.areas = response.data;
    });
  },
  methods: {
    getGeom() {
      this.axios
        .get("http://127.0.0.1:8000/geo/" + this.selected)
        .then((response) => {
          if (this.geom) {
            this.map.removeLayer(this.geom);
          }
          this.geom = L.geoJSON(response.data.geom).addTo(this.map);
          this.map.fitBounds(this.geom.getBounds());
        });
    },
    removeLayer() {
      this.map.removeLayer(this.geom);
    },
    uploadFile() {
      this.uploadGeom = this.$refs.file.files[0];
    },
    submitFile() {
      const formData = new FormData();
      formData.append("file", this.uploadGeom);
      formData.append("description", this.description);
      const headers = { "Content-Type": "multipart/form-data" };
      this.axios
        .post("http://127.0.0.1:8000/geo/", formData, { headers })
        .then((res) => {
          this.areas.push(res.data);
          this.message = "Succesfully uploaded geometry to database.";

          this.axios
            .get("http://127.0.0.1:8000/geo/" + res.data.catch_area_id)
            .then((response) => {
              if (this.geom) {
                this.map.removeLayer(this.geom);
              }
              this.geom = L.geoJSON(response.data.geom).addTo(this.map);
              this.map.fitBounds(this.geom.getBounds());
            });
        })
        .catch(() => {
          this.message = "Error with upload, file format not GeoJSON?";
        });
    },
  },
};
</script>

<style>
#map {
  height: 500px;
  padding: 20px;
}
</style>
