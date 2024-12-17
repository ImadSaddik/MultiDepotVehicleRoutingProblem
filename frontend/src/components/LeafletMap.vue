<template>
  <div id="map"></div>
</template>

<script>
import L from "leaflet";
import { toRaw } from "vue";

import { dataStore } from "@/store/dataStore";

export default {
  name: "LeafletMap",
  props: {
    employeeData: [],
    busData: [],
    companyData: {},
    showEmployees: true,
    showBuses: true,
    routeDisplay: {
      type: Object,
      default: () => ({ showFullRoute: true, selectedSegment: 0 }),
    },
  },
  setup() {
    const store = dataStore();
    return { store };
  },
  data() {
    return {
      map: null,
      centerCoordinates: [35.754085, -5.828958],
      zoomLevel: 14,
      employeeLayer: null,
      busLayer: null,
      companyLayer: null,
      routeLayer: null,
      employeeIcon: null,
      busIcon: null,
      companyIcon: null,
      arrowMarker: null,
    };
  },
  watch: {
    employeeData: {
      handler() {
        if (this.map && this.employeeLayer) {
          this.updateEmployeeMarkers();
        }
      },
      deep: true,
    },
    busData: {
      handler() {
        if (this.map && this.busLayer) {
          this.updateBusMarkers();
        }
      },
      deep: true,
    },
    companyData: {
      handler() {
        if (this.map && this.companyLayer) {
          this.updateCompanyMarker();
        }
      },
      deep: true,
    },
    showEmployees(val) {
      if (this.employeeLayer) {
        if (val) toRaw(this.employeeLayer).addTo(toRaw(this.map));
        else toRaw(this.employeeLayer).remove();
      }
    },
    showBuses(val) {
      if (this.busLayer) {
        if (val) toRaw(this.busLayer).addTo(toRaw(this.map));
        else toRaw(this.busLayer).remove();
      }
    },
    "store.sidePanelStep"(step) {
      this.handleStepChange(step);
    },
    "store.selectedCluster"() {
      this.updateRouteIfVisible();
    },
    routeDisplay: {
      handler(newValue) {
        if (newValue) {
          this.store.setRouteDisplayMode(newValue);
          this.updateRouteIfVisible();
        }
      },
      deep: true,
    },
  },
  mounted() {
    this.initializeMap();
    this.initializeIcons();
    this.initializeLayers();
  },
  methods: {
    initializeMap() {
      this.map = L.map("map", { attributionControl: false }).setView(
        this.centerCoordinates,
        this.zoomLevel
      );

      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14">
          <path d="M 0,7 L 12,0 L 12,14 Z" fill="blue" opacity="0.7"/>
        </svg>
      `;

      this.arrowMarker = encodeURI("data:image/svg+xml;base64," + btoa(svg));

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>",
      }).addTo(toRaw(this.map));
      L.control.attribution({ position: "bottomleft" }).addTo(toRaw(this.map));
    },
    initializeIcons() {
      this.employeeIcon = L.divIcon({
        html: `
          <div class="marker-background employee-bg">
            <span class="material-icons">person</span>
          </div>
        `,
        className: "employee-marker",
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24],
      });

      this.busIcon = L.divIcon({
        html: `
          <div class="marker-background bus-bg">
            <span class="material-icons">directions_bus</span>
          </div>
        `,
        className: "bus-marker",
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24],
      });

      this.companyIcon = L.divIcon({
        html: `
          <div class="marker-background company-bg">
            <span class="material-icons">business</span>
          </div>
        `,
        className: "company-marker",
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24],
      });
    },
    initializeLayers() {
      this.employeeLayer = L.layerGroup().addTo(toRaw(this.map));
      this.busLayer = L.layerGroup().addTo(toRaw(this.map));
      this.companyLayer = L.layerGroup().addTo(toRaw(this.map));
      this.routeLayer = L.layerGroup().addTo(toRaw(this.map));
    },
    updateEmployeeMarkers() {
      const rawLayer = toRaw(this.employeeLayer);
      rawLayer.clearLayers();

      this.employeeData.forEach((employee) => {
        const marker = L.marker([employee.latitude, employee.longitude], {
          icon: toRaw(this.employeeIcon),
        }).bindPopup(`
            <strong>Employee</strong><br>
            ID: ${employee.id}<br>
            Latitude: ${employee.latitude.toFixed(6)}<br>
            Longitude: ${employee.longitude.toFixed(6)}
          `);
        rawLayer.addLayer(marker);
      });
    },
    updateBusMarkers() {
      const rawLayer = toRaw(this.busLayer);
      rawLayer.clearLayers();

      this.busData.forEach((bus) => {
        const marker = L.marker([bus.latitude, bus.longitude], {
          icon: toRaw(this.busIcon),
        }).bindPopup(`
            <strong>Bus</strong><br>
            ID: ${bus.id}<br>
            Latitude: ${bus.latitude.toFixed(6)}<br>
            Longitude: ${bus.longitude.toFixed(6)}
          `);
        rawLayer.addLayer(marker);
      });
    },
    updateCompanyMarker() {
      const companyData = toRaw(this.store.companyData);
      if (Object.keys(companyData).length === 0) {
        return;
      }

      const rawLayer = toRaw(this.companyLayer);
      rawLayer.clearLayers();

      const marker = L.marker([companyData.latitude, companyData.longitude], {
        icon: toRaw(this.companyIcon),
      }).bindPopup(`
          <strong>Company</strong><br>
          Latitude: ${companyData.latitude.toFixed(6)}<br>
          Longitude: ${companyData.longitude.toFixed(6)}
        `);
      rawLayer.addLayer(marker);
    },
    updateRouteLayer() {
      const rawLayer = toRaw(this.routeLayer);
      rawLayer.clearLayers();

      const clusterData = toRaw(
        this.store.optimizedData[this.store.selectedCluster]
      );
      const routeSegments = clusterData["route_segments"];
      const busNode = clusterData["bus_node"];

      const displayMode = this.store.routeDisplayMode || {
        showFullRoute: true,
        selectedSegment: 0,
      };

      if (displayMode.showFullRoute) {
        this.centerMapOnLocation(
          busNode.latitude,
          busNode.longitude,
          displayMode
        );
        this.drawAllSegments(routeSegments, rawLayer);
      } else {
        const selectedSegment = routeSegments[displayMode.selectedSegment];
        const segmentStartingPoint = selectedSegment.coordinates[0];

        this.centerMapOnLocation(
          segmentStartingPoint.latitude,
          segmentStartingPoint.longitude,
          displayMode
        );
        this.drawSingleSegment(selectedSegment, rawLayer);
      }
    },
    drawAllSegments(segments, layer) {
      segments.forEach((segment) => {
        const coordinates = segment.coordinates.map((location) => [
          location.latitude,
          location.longitude,
        ]);

        this.drawSegment(coordinates, layer);
      });
    },
    drawSingleSegment(segment, layer) {
      if (!segment) return;

      const coordinates = segment.coordinates.map((location) => [
        location.latitude,
        location.longitude,
      ]);

      this.drawSegment(coordinates, layer);
    },
    drawSegment(coordinates, layer) {
      const polylineBorder = L.polyline(coordinates, {
        color: "#000000",
        weight: 9,
        opacity: 1,
        smoothFactor: 1.25,
      });

      const polyline = L.polyline(coordinates, {
        weight: 7,
        opacity: 1,
        smoothFactor: 1.25,
        stroke: true,
        color: "#FFA500",
      });

      this.addArrowsToSegment(polyline, layer);

      layer.addLayer(polylineBorder);
      layer.addLayer(polyline);
    },
    addArrowsToSegment(polyline, layer) {
      const points = polyline.getLatLngs();
      const arrowsPerSegment = 5;
      const step = (points.length - 1) / (arrowsPerSegment + 1);

      for (let i = 1; i <= arrowsPerSegment; i++) {
        const index = Math.floor(step * i);
        const prevIndex = Math.floor(index - 1);

        if (prevIndex >= 0 && index < points.length) {
          const rotationAngle = this.getRotationAngle(
            points[index],
            points[prevIndex]
          );
          const midPoint = L.latLng(
            (points[prevIndex].lat + points[index].lat) / 2,
            (points[prevIndex].lng + points[index].lng) / 2
          );

          const arrowIcon = L.divIcon({
            html: `<div style="
              width: 14px;
              height: 14px;
              background-image: url(${this.arrowMarker});
              transform: rotate(${rotationAngle}deg);
            "></div>`,
            className: "arrow-marker",
            iconSize: [14, 14],
            iconAnchor: [7, 7],
          });

          L.marker(midPoint, { icon: arrowIcon }).addTo(layer);
        }
      }
    },
    getRotationAngle(p1, p2) {
      return (
        (Math.atan2(p2.lng - p1.lng, p1.lat - p2.lat) * 180) / Math.PI - 90
      );
    },
    centerMapOnLocation(latitude, longitude, displayMode) {
      const customZoomLevel = displayMode.showFullRoute ? 16 : 18;
      const easeLinearity = displayMode.showFullRoute ? 0.25 : 1;
      const duration = displayMode.showFullRoute ? 1 : 0.5;
      if (this.map) {
        toRaw(this.map).flyTo([latitude, longitude], customZoomLevel, {
          duration: duration,
          easeLinearity: easeLinearity,
        });
      }
    },
    handleStepChange(step) {
      this.hideAllLayers();

      switch (step) {
        case 2:
          this.showDataLayers();
          break;
        case 4:
          this.showOptimizationResults();
          break;
      }
    },
    hideAllLayers() {
      const rawMap = toRaw(this.map);
      [
        this.employeeLayer,
        this.busLayer,
        this.companyLayer,
        this.routeLayer,
      ].forEach((layer) => layer && toRaw(layer).remove(rawMap));
    },
    showDataLayers() {
      const rawMap = toRaw(this.map);
      if (this.employeeLayer && this.showEmployees) {
        toRaw(this.employeeLayer).addTo(rawMap);
      }
      if (this.busLayer && this.showBuses) {
        toRaw(this.busLayer).addTo(rawMap);
      }
      if (this.companyLayer) {
        toRaw(this.companyLayer).addTo(rawMap);
      }
    },
    showOptimizationResults() {
      this.showDataLayers();
      if (this.routeLayer) {
        this.updateRouteLayer();
        toRaw(this.routeLayer).addTo(toRaw(this.map));
      }
    },
    updateRouteIfVisible() {
      if (this.map && this.routeLayer && this.store.sidePanelStep === 4) {
        this.updateRouteLayer();
      }
    },
  },
};
</script>

<style>
#map {
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  position: absolute;
}

@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

.employee-marker,
.bus-marker {
  display: block;
  background: none;
}

.marker-background {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.employee-bg {
  background: #2196f3;
  border: 2px solid #1976d2;
}

.bus-bg {
  background: #4caf50;
  border: 2px solid #388e3c;
}

.company-bg {
  background: #f44336;
  border: 2px solid #d32f2f;
}

.marker-background .material-icons {
  transform: rotate(45deg);
  color: white;
  font-size: 0.75rem;
  filter: drop-shadow(1px 1px 1px rgba(0, 0, 0, 0.3));
}

.arrow-marker {
  background: none;
  border: none;
}
</style>
