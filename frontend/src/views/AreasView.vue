<template>
  <div class="rules">
    <div
      v-for="area in areas"
      :value="area.catch_area_id"
      :key="area.description"
    >
      <router-link
        :to="{ name: 'rules', params: { areaID: area.catch_area_id } }"
        >{{ area.description }}</router-link
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "AreasView",
  data() {
    return {
      areas: [],
    };
  },
  mounted() {
    this.axios.get("http://127.0.0.1:8000/api/catchareas/").then((response) => {
      this.areas = response.data;
    });
  },
  methods: {},
};
</script>
<!-- <style>
@media (min-width: 1024px) {
  .rules {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style> -->
