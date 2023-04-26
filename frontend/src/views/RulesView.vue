<template>
  <div>
    <div id="map"></div>
    <div v-if="!rules.length">
      <span><h3>No rules have been added to this geometry</h3></span>
    </div>
    <div v-else>
      <div class="rules">
        <table>
          <thead>
            <tr>
              <th>Area Description</th>
              <th>Regulation Type</th>
              <th>Start Datetime</th>
              <th>End Datetime</th>
              <th>Species</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rule in rules" :key="rule">
              <td>{{ rule.description }}</td>
              <td>{{ rule.regulation_type_code }}</td>
              <td>
                {{
                  $dayjs(rule.start_rule_datetime).format("YYYY-MM-DD h:mma")
                }}
              </td>
              <td>
                {{ $dayjs(rule.end_rule_datetime).format("YYYY-MM-DD h:mma") }}
              </td>
              <td>{{ rule.common_name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div>
      <button @click="addRule = !addRule">Add Rule</button>

      <div v-if="addRule">
        <div>
          <h3>Choose Regulation Type</h3>
          <select v-model="selectedReg" style="width: 100%">
            <option
              v-for="reg in regTypes"
              :value="reg.regulation_type_id"
              :key="reg"
            >
              {{ reg.regulation_type_code }}
            </option>
          </select>
        </div>
        <div>
          <h3>Choose Species</h3>
          <select v-model="selectedSpecies" style="width: 100%">
            <option
              v-for="specie in species"
              :value="specie.species_id"
              :key="specie"
            >
              {{ specie.common_name }}
            </option>
          </select>
        </div>
        <div>
          <h3>Choose Date Range</h3>
          <Datepicker v-model="date" range />
        </div>
        <div><button @click="saveRule()">Save</button></div>
      </div>
    </div>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

export default {
  components: { Datepicker },
  data() {
    return {
      area: null,
      species: [],
      regTypes: [],
      rules: [],
      selectedReg: null,
      selectedSpecies: null,
      addRule: null,
      date: null,
    };
  },
  mounted() {
    this.area = this.$route.params.areaID;
    this.map = L.map("map");
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.map);
    this.axios
      .get("http://127.0.0.1:8000/geo/" + this.area)
      .then((response) => {
        this.geom = L.geoJSON(response.data.geom).addTo(this.map);
        this.map.fitBounds(this.geom.getBounds());
      });
    this.axios
      .get("http://127.0.0.1:8000/api/rules/" + this.area)
      .then((response) => {
        this.rules = response.data;
      });
    this.axios
      .get("http://127.0.0.1:8000/api/regulationtypes/")
      .then((response) => {
        this.regTypes = response.data;
      });
    this.axios.get("http://127.0.0.1:8000/api/species/").then((response) => {
      this.species = response.data;
    });
  },
  methods: {
    saveRule() {
      this.rule = {
        catch_area_id: this.area,
        regulation_type_id: this.selectedReg,
        start_rule_datetime: this.date[0],
        end_rule_datetime: this.date[1],
        species_id: this.selectedSpecies,
      };
      //console.log(JSON.stringify(this.rule));
      const headers = { "Content-Type": "application/json" };
      this.axios
        .post("http://127.0.0.1:8000/api/rules/", JSON.stringify(this.rule), {
          headers,
        })
        .then((response) => {
          this.axios
            .get("http://127.0.0.1:8000/api/rules/" + this.area)
            .then((response) => {
              this.rules = response.data;
            });
        });
    },
  },
};
</script>
<style>
#map {
  height: 300px;
  padding: 20px;
}
</style>
<!-- <style>
@media (min-width: 1024px) {
  .rules {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style> -->
