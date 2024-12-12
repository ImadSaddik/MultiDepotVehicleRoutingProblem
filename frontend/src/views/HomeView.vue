<template>
  <LeafletMap 
    :employeeData="employeeData"
    :busData="busData"
    :showEmployees
  />
  <SidePanel 
    @data-updated="handleUpdatedData"
    @employee-toggle-switch-change="handleEmployeeToggleSwitchChange"
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
      showEmployees: true,
    };
  },
  methods: {
    handleUpdatedData({ employeeData, busData }) {
      this.employeeData = employeeData;
      this.busData = busData;
    },
    handleEmployeeToggleSwitchChange(value) {
      this.showEmployees = value;
    }
  }
};
</script>

<style scoped>
</style>
