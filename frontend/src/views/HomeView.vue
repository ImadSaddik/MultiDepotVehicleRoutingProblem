<template>
  <LeafletMap 
    :employeeData="employeeData"
    :busData="busData"
    :companyData="companyData"
    :showEmployees
    :showBuses
  />
  <SidePanel 
    @sliced-data="handleSlicedData"
    @employee-toggle-switch-change="handleEmployeeToggleSwitchChange"
    @bus-toggle-switch-change="handleBusToggleSwitchChange"
  />
</template>

<script>
import LeafletMap from '@/components/LeafletMap.vue';
import SidePanel from '@/components/SidePanel.vue';

export default {
  name: "HomeView",
  components: {
    LeafletMap,
    SidePanel
  },
  data() {
    return {
      employeeData: [],
      busData: [],
      companyData: {},
      showEmployees: true,
      showBuses: true
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
    }
  }
};
</script>

<style scoped>
</style>
