<template>
  <div class="step-container">
    <h1>Routing solver</h1>
    <h2>Results visualization</h2>

    <p>
      The results are displayed in the map. You can cycle through each bus route to see the optimized route.
    </p>

    <Button
      label="Back"
      icon="pi pi-arrow-left"
      class="back-button"
      @click="goToPreviousStep"
    />
  </div>
</template>

<script>
import { dataStore } from "@/store/dataStore";

import Button from "primevue/button";

export default {
  name: "SidePanelStep4",
  components: {
    Button,
  },
  setup() {
    const store = dataStore();
    return { store };
  },
  data() {
    return {
    };
  },
  methods: {
    goToPreviousStep() {
      this.$emit("previous-step");
    },
  },
};
</script>

<style scoped>
.back-button {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
</style>
