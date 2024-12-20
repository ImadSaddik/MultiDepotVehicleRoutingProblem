<template>
  <LeafletMap 
    :employeeData="employeeData"
    :busData="busData"
    :companyData="companyData"
    :routeDisplayMode="routeDisplayMode"
    :showEmployees="showEmployees"
    :showBuses="showBuses"
  />

  <div class="action-buttons">
    <Button 
      :icon="isDarkMode ? 'pi pi-sun' : 'pi pi-moon'"
      class="theme-button" 
      @click="toggleAppTheme" 
    />

    <Button 
      :icon="isSidePanelOpen ? 'pi pi-chevron-right' : 'pi pi-chevron-left'" 
      class="toggle-button" 
      @click="toggleSidePanelVisibility" 
    />
  </div>

  <transition name="slide-panel" mode="out-in">
    <SidePanel
      v-show="isSidePanelOpen"
      @sliced-data="handleSlicedData"
      @employee-toggle-switch-change="handleEmployeeToggleSwitchChange"
      @bus-toggle-switch-change="handleBusToggleSwitchChange"
      @cluster-selected="handleClusterData"
    />
  </transition>
</template>

<script>
import Button from 'primevue/button';
import SidePanel from '@/components/SidePanel.vue';
import LeafletMap from '@/components/LeafletMap.vue';

export default {
  name: "HomeView",
  components: {
    Button,
    SidePanel,
    LeafletMap
  },
  data() {
    return {
      employeeData: [],
      busData: [],
      companyData: {},
      showEmployees: true,
      showBuses: true,
      isSidePanelOpen: true,
      routeDisplayMode: {
        showFullRoute: true,
        selectedSegment: 0,
      },
      isDarkMode: false,
    };
  },
  methods: {
    handleSlicedData(data) {
      this.updateData(data);
    },
    handleClusterData(data) {
      this.updateData(data);
    },
    updateData({ employeeData, busData, companyData, routeDisplayMode }) {
      this.employeeData = employeeData;
      this.busData = busData;
      this.companyData = companyData;
      this.routeDisplayMode = routeDisplayMode;
    },
    handleEmployeeToggleSwitchChange(value) {
      this.showEmployees = value;
    },
    handleBusToggleSwitchChange(value) {
      this.showBuses = value;
    },
    toggleSidePanelVisibility() {
      this.isSidePanelOpen = !this.isSidePanelOpen;
    }
  }
};
</script>

<style scoped>
.action-buttons {
  display: flex;

  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 2000;
}

.theme-button {
  margin-right: 1rem;
}

.slide-panel-enter-active,
.slide-panel-leave-active {
  transition: transform 0.3s ease-in-out;
}
.slide-panel-enter-from {
  transform: translateX(100%);
}
.slide-panel-leave-to {
  transform: translateX(100%);
}
</style>
