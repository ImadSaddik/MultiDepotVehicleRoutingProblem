<template>
  <div id="map"></div>
</template>

<script>
import L from "leaflet";
import { toRaw } from 'vue';

import { dataStore } from "@/store/dataStore";

export default {
  name: "LeafletMap",
  props: {
    employeeData: [],
    busData: [],
    companyData: {},
    showEmployees: true,
    showBuses: true
  },
  setup() {
    const store = dataStore()
    return { store }
  },
  data() {
    return {
      map: null,
      centerCoordinates: [35.754085, -5.828958],
      zoomLevel: 14,
      employeeLayer: null,
      busLayer: null,
      companyLayer: null,
      employeeIcon: null,
      busIcon: null,
      companyIcon: null
    };
  },
  watch: {
    employeeData: {
      handler() {
        if (this.map && this.employeeLayer) {
          this.updateEmployeeMarkers();
        }
      },
      deep: true
    },
    busData: {
      handler() {
        if (this.map && this.busLayer) {
          this.updateBusMarkers();
        }
      },
      deep: true
    },
    companyData: {
      handler() {
        if (this.map && this.companyLayer) {
          this.updateCompanyMarker();
        }
      },
      deep: true
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
    }
  },
  mounted() {
    this.initializeMap();
    this.initializeIcons();
    this.initializeLayers();
  },
  methods: {
    initializeMap() {
      this.map = L.map("map", { attributionControl: false }).setView(this.centerCoordinates, this.zoomLevel);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>"
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
        className: 'employee-marker',
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
      });
      
      this.busIcon = L.divIcon({
        html: `
          <div class="marker-background bus-bg">
            <span class="material-icons">directions_bus</span>
          </div>
        `,
        className: 'bus-marker',
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
      });

      this.companyIcon = L.divIcon({
        html: `
          <div class="marker-background company-bg">
            <span class="material-icons">business</span>
          </div>
        `,
        className: 'company-marker',
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
      });
    },
    initializeLayers() {
      this.employeeLayer = L.layerGroup().addTo(toRaw(this.map));
      this.busLayer = L.layerGroup().addTo(toRaw(this.map));
      this.companyLayer = L.layerGroup().addTo(toRaw(this.map));

      this.updateEmployeeMarkers();
      this.updateBusMarkers();
      this.updateCompanyMarker();
    },
    updateEmployeeMarkers() {
      const rawLayer = toRaw(this.employeeLayer);
      rawLayer.clearLayers();
      
      this.employeeData.forEach(employee => {
        const marker = L.marker([employee.Latitude, employee.Longitude], { icon: toRaw(this.employeeIcon) })
          .bindPopup(`
            <strong>Employee</strong><br>
            ID: ${employee.ID}<br>
            Latitude: ${employee.Latitude.toFixed(6)}<br>
            Longitude: ${employee.Longitude.toFixed(6)}
          `);
        rawLayer.addLayer(marker);
      });
    },
    updateBusMarkers() {
      const rawLayer = toRaw(this.busLayer);
      rawLayer.clearLayers();

      this.busData.forEach(bus => {
        const marker = L.marker([bus.Latitude, bus.Longitude], { icon: toRaw(this.busIcon) })
          .bindPopup(`
            <strong>Bus</strong><br>
            ID: ${bus.ID}<br>
            Latitude: ${bus.Latitude.toFixed(6)}<br>
            Longitude: ${bus.Longitude.toFixed(6)}
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

      const marker = L.marker([companyData.latitude, companyData.longitude], { icon: toRaw(this.companyIcon) })
        .bindPopup(`
          <strong>Company</strong><br>
          Latitude: ${companyData.latitude.toFixed(6)}<br>
          Longitude: ${companyData.longitude.toFixed(6)}
        `);
      rawLayer.addLayer(marker);
    }
  }
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

@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.employee-marker, .bus-marker {
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
  background: #2196F3;
  border: 2px solid #1976D2;
}

.bus-bg {
  background: #4CAF50;
  border: 2px solid #388E3C;
}

.company-bg {
  background: #F44336;
  border: 2px solid #D32F2F;
}

.marker-background .material-icons {
  transform: rotate(45deg);
  color: white;
  font-size: 0.75rem;
  filter: drop-shadow(1px 1px 1px rgba(0,0,0,0.3));
}
</style>
