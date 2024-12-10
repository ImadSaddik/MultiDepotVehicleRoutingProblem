<template>
  <LeafletMap />
  <SidePanel />
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
    };
  },
};
</script>

<style scoped>
</style>
