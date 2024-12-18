<template>
  <router-view/>
</template>

<style>
:root {
  font-family: "Roboto Condensed", sans-serif;
}

h1 {
  font-size: 2rem;
  margin: 0;
}

.step-container {
  height: 100%;
  width: 100%;
  position: relative;
  padding: 1rem;
}

.step-container .p-divider.custom-divider {
  width: 60%;
  margin: 1rem auto;
}

.leaflet-control-zoom-in,
.leaflet-control-zoom-out {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: var(--p-button-primary-color) !important;
  background: var(--p-button-primary-background) !important;
  border: 1px solid #888 !important;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
  width: 2.25rem !important;
  height: 2.25rem !important;
  line-height: 2rem !important;
  border-radius: var(--p-button-border-radius) !important;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s !important;
}

.leaflet-control-zoom-in.leaflet-disabled,
.leaflet-control-zoom-out.leaflet-disabled {
  pointer-events: none;
  opacity: 0.5;
}

.leaflet-control-zoom-out {
  margin-top: 0.5rem;
}

.leaflet-control-zoom-in:hover,
.leaflet-control-zoom-out:hover {
  background-color: var(--p-primary-600) !important;
  border-color: var(--p-primary-600) !important;
}

.leaflet-control-zoom {
  border: 0px !important;
}
</style>