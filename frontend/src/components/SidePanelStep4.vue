<template>
  <div class="step-container">
    <Toast position="bottom-left" />

    <h1>Routing solver</h1>
    <h2>Results visualization</h2>

    <p>
      The results are displayed in the map. You can cycle through each bus to see the optimized route.
    </p>

    <div class="cluster-selection-buttons">
      <Button 
        :disabled="selectedCluster === 0"
        icon="pi pi-chevron-left"
        class="toggle-button"
        @click="showPreviousCluster" 
      />

      <p>Bus N° {{ selectedCluster }}</p>

      <Button 
        :disabled="selectedCluster === store.optimizedData.length - 1"
        icon="pi pi-chevron-right"
        class="toggle-button" 
        @click="showNextCluster" 
      />
    </div>

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

import Toast from "primevue/toast";
import Button from "primevue/button";

export default {
  name: "SidePanelStep4",
  components: {
    Toast,
    Button,
  },
  setup() {
    const store = dataStore();
    return { store };
  },
  data() {
    return {
      selectedCluster: 0,
    };
  },
  methods: {
    goToPreviousStep() {
      this.$emit("previous-step");
    },
    showNextCluster() {
      if (this.selectedCluster === this.store.optimizedData.length - 1) {
        this.$toast.add({
          severity: "error",
          summary: "Error",
          detail: "You are already at the last cluster",
          life: 5000,
        });
        return;
      }

      this.selectedCluster = this.selectedCluster + 1;
    },
    showPreviousCluster() {
      if (this.selectedCluster === 0) {
        this.$toast.add({
          severity: "error",
          summary: "Error",
          detail: "You are already at the first cluster",
          life: 5000,
        });
        return;
      }

      this.selectedCluster = this.selectedCluster - 1;
    },
  },
};
</script>

<style scoped>
.cluster-selection-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.back-button {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
</style>
