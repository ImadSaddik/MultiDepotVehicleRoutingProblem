<template>
  <LeafletMap 
    :employeeData="employeeData"
    :busData="busData"
    :companyData="companyData"
    :showEmployees
    :showBuses
  />
  <Button 
    :icon="isSidePanelOpen ? 'pi pi-chevron-right' : 'pi pi-chevron-left'" 
    class="toggle-button" 
    @click="toggleSidePanelVisibility" 
  />
  <transition name="slide-panel" mode="out-in">
    <SidePanel
      v-if="isSidePanelOpen"
      @sliced-data="handleSlicedData"
      @employee-toggle-switch-change="handleEmployeeToggleSwitchChange"
      @bus-toggle-switch-change="handleBusToggleSwitchChange"
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
      isSidePanelOpen: true
    };
  },
  methods: {
    handleSlicedData({ employeeData, busData, companyData }) {
      this.employeeData = employeeData;
      this.busData = busData;
      this.companyData = companyData;
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
.toggle-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 2000;
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
