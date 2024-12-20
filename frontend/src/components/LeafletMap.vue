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
    routeDisplayMode: {
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
      arrowMarkerInstance: null,
      animationFrame: null,
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
    routeDisplayMode: {
      handler(newValue) {
        if (newValue) {
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
      this.map = L.map("map", {
        attributionControl: false,
        zoomSnap: 0.25,
        zoomDelta: 0.5,
        wheelPxPerZoomLevel: 120, 
      }).setView(this.centerCoordinates, this.zoomLevel);

      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28">
          <polyline points="4,4 14,14 4,24" fill="none" stroke="black" stroke-width="3"/>
        </svg>
      `;

      this.arrowMarker = encodeURI("data:image/svg+xml;base64," + btoa(svg));

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>",
      }).addTo(toRaw(this.map));
      L.control.attribution({ position: "bottomleft" }).addTo(toRaw(this.map));

      this.map.on('zoomend', this.updateZoomControls);
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

      if (this.routeDisplayMode.showFullRoute) {
        this.centerMapOnLocation(
          busNode.latitude,
          busNode.longitude,
          this.routeDisplayMode
        );
        this.drawAllSegments(routeSegments, rawLayer);
        const coordinates = this.getCoordinatesFromSegments(routeSegments);
        this.animateArrowAlongPath(coordinates, rawLayer);
      } else {
        const selectedSegment = routeSegments[this.routeDisplayMode.selectedSegment];
        const segmentStartingPoint = selectedSegment.coordinates[0];

        this.centerMapOnLocation(
          segmentStartingPoint.latitude,
          segmentStartingPoint.longitude,
          this.routeDisplayMode
        );
        this.drawSingleSegment(selectedSegment, rawLayer);
        const coordinates = selectedSegment.coordinates.map((location) => [
          location.latitude,
          location.longitude,
        ]);
        this.animateArrowAlongPath(coordinates, rawLayer);
      }
    },
    getCoordinatesFromSegments(segments) {
      const coordinates = [];
      segments.forEach((segment) => {
        segment.coordinates.forEach((location) => {
          coordinates.push([location.latitude, location.longitude]);
        });
      });
      return coordinates;
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

      this.drawSegment(coordinates, layer, segment);
    },
    drawSegment(coordinates, layer, segment = null) {
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

      if (segment) {
        const minutes = Math.floor(segment.duration / 60);
        const seconds = Math.floor(segment.duration % 60);
        const formattedDuration = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        const tooltipContent = `
          <strong>Segment info</strong><br>
          Distance: ${segment.distance} m<br>
          Duration: ${formattedDuration} min<br>
          From Node ID: ${segment.source_node_id}<br>
          To Node ID: ${segment.destination_node_id}
        `;
        polyline.bindTooltip(tooltipContent, { sticky: true });
      }

      layer.addLayer(polylineBorder);
      layer.addLayer(polyline);
    },
    centerMapOnLocation(latitude, longitude, routeDisplayMode) {
      const customZoomLevel = routeDisplayMode.showFullRoute ? 16 : 17;
      const easeLinearity = routeDisplayMode.showFullRoute ? 0.25 : 1;
      const duration = routeDisplayMode.showFullRoute ? 1 : 0.5;
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
    updateZoomControls() {
      const zoomInButton = document.querySelector('.leaflet-control-zoom-in');
      const zoomOutButton = document.querySelector('.leaflet-control-zoom-out');
      const currentZoom = this.map.getZoom();

      if (currentZoom >= 18) {
        zoomInButton.classList.add('leaflet-disabled');
      } else {
        zoomInButton.classList.remove('leaflet-disabled');
      }

      if (currentZoom <= 0) {
        zoomOutButton.classList.add('leaflet-disabled');
      } else {
        zoomOutButton.classList.remove('leaflet-disabled');
      }
    },
    animateArrowAlongPath(coordinates, layer) {
      if (this.animationFrame) {
        cancelAnimationFrame(this.animationFrame);
      }
      if (this.arrowMarkerInstance) {
        this.arrowMarkerInstance.remove();
      }

      const arrowMarker = L.marker(coordinates[0], { icon: L.divIcon() }).addTo(layer);
      this.arrowMarkerInstance = arrowMarker;

      let totalDistance = 0;
      for (let i = 1; i < coordinates.length; i++) {
        totalDistance += this.map.distance(coordinates[i - 1], coordinates[i]);
      }

      const arrowSpeedInMeterPerSecond = 100;
      const totalDurationInSeconds = totalDistance / arrowSpeedInMeterPerSecond;
      const startTime = performance.now();

      const animate = () => {
        const currentTime = performance.now();
        const elapsedTimeInSeconds = (currentTime - startTime) / 1000;
        let progress = (elapsedTimeInSeconds % totalDurationInSeconds) / totalDurationInSeconds;

        const latlng = this.interpolatePointOnLine(coordinates, progress);
        const latlngObject = { lat: latlng[0], lng: latlng[1] };
        arrowMarker.setLatLng(latlng);

        const nextProgress = (progress + 0.0001) % 1;
        const nextLatLng = this.interpolatePointOnLine(coordinates, nextProgress);
        const nextLatLngObject = { lat: nextLatLng[0], lng: nextLatLng[1] };
        const angle = this.getRotationAngle(latlngObject, nextLatLngObject);

        const arrowIcon = L.divIcon({
          html: `<div style="
            width: 28px;
            height: 28px;
            background-image: url(${this.arrowMarker});
            transform: rotate(${angle}deg);
          "></div>`,
          className: "arrow-marker",
          iconSize: [28, 28],
          iconAnchor: [14, 14],
        });

        arrowMarker.setIcon(arrowIcon);

        this.animationFrame = requestAnimationFrame(animate);
      };
      animate();
    },
    interpolatePointOnLine(coordinates, progress) {
      let totalDistance = 0;
      const distances = [];

      for (let i = 1; i < coordinates.length; i++) {
        const distance = this.map.distance(coordinates[i - 1], coordinates[i]);
        distances.push(distance);
        totalDistance += distance;
      }

      let accumulatedDistance = 0;
      const targetDistance = progress * totalDistance;

      for (let i = 0; i < distances.length; i++) {
        if (accumulatedDistance + distances[i] >= targetDistance) {
          const segmentProgress =
            (targetDistance - accumulatedDistance) / distances[i];

          const lat =
            coordinates[i][0] +
            segmentProgress * (coordinates[i + 1][0] - coordinates[i][0]);
          const lng =
            coordinates[i][1] +
            segmentProgress * (coordinates[i + 1][1] - coordinates[i][1]);

          return [lat, lng];
        }

        accumulatedDistance += distances[i];
      }

      return coordinates[coordinates.length - 1];
    },
    getRotationAngle(p1, p2) {
      return (
        (Math.atan2(p2.lat - p1.lat, p1.lng - p2.lng) * 180) / Math.PI - 180
      );
    },
  },
  beforeDestroy() {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
    if (this.arrowMarkerInstance) {
      this.arrowMarkerInstance.remove();
    }
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
