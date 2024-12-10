<template>
  <div id="map"></div>
</template>

<script>
import L from "leaflet";

export default {
  name: "LeafletMap",
  components: {},
  data() {
    return {
      map: null,
      centerCoordinates: [51.505, -0.09],
      zoomLevel: 13,
    };
  },
  mounted() {
    this.map = L.map("map").setView(this.centerCoordinates, this.zoomLevel);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>",
      attributionControl: false,
    }).addTo(this.map);
    L.control
      .attribution({
        position: "bottomleft",
      })
      .addTo(this.map);
  },
};
</script>

<style scoped>
#map {
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  position: absolute;
}
</style>
