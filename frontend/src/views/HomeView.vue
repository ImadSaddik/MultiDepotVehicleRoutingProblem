<template>
  <LeafletMap 
    :employeeData="employeeData"
    :busData="busData"
  />
  <SidePanel 
    @data-updated="handleUpdatedData"
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
    };
  },
  methods: {
    handleUpdatedData({ employeeData, busData }) {
      this.employeeData = employeeData;
      this.busData = busData;
    },
  }
};
</script>

<style scoped>
</style>
