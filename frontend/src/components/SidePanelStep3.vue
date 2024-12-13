<template>
  <div class="step-container">
    <h1>Routing solver</h1>
    <h2>Optimization step</h2>

    <p>
      Choose a routing solver to optimize the routes. Once selected, click on
      the <b>Optimize</b> button to start the optimization process.
    </p>

    <label class="custom-label" for="solverSelector">Solver</label>
    <Select
      id="solverSelector"
      v-model="selectedSolver"
      :options="solvers"
      showClear
      optionLabel="name"
      placeholder="Select a solver"
      class="custom-selector"
      :class="{ 'p-invalid': isSolverInvalid }"
    />

    <Button
      label="Optimize"
      iconPos="right"
      class="optimize-button"
      @click="startSolver"
    />

    <Toast position="bottom-left" />

    <div class="navigation-buttons">
      <Button
        label="Back"
        icon="pi pi-arrow-left"
        class="back-button"
        @click="goToPreviousStep"
      />
      <Button
        :disabled="!isResultAvailable"
        label="Next"
        icon="pi pi-arrow-right"
        iconPos="right"
        class="next-button"
        @click="goToNextStep"
      />
    </div>
  </div>
</template>

<script>
import { dataStore } from "@/store/dataStore";

import Toast from "primevue/toast";
import Button from "primevue/button";
import Select from "primevue/select";
import Divider from "primevue/divider";

export default {
  name: "SidePanelStep3",
  components: {
    Toast,
    Button,
    Select,
    Divider,
  },
  setup() {
    const store = dataStore();
    return { store };
  },
  data() {
    return {
      selectedSolver: null,
      solvers: [
        { name: "Greedy TSP", value: "greedy_tsp" },
        { name: "Simulated annealing TSP", value: "simulated_annealing_tsp" },
        { name: "Threshold accepting TSP", value: "threshold_accepting_tsp" },
      ],
      isResultAvailable: false,
      isSolverInvalid: false,
    };
  },
  methods: {
    goToNextStep() {
      this.$emit("next-step");
    },
    goToPreviousStep() {
      this.$emit("previous-step");
    },
    startSolver() {
      if (!this.selectedSolver) {
        this.isSolverInvalid = true;
        this.$toast.add({
          severity: "error",
          summary: "Validation error",
          detail: "Please select a solver",
          life: 5000,
        });
        return;
      }
      this.isSolverInvalid = false;
      console.log("Starting solver with selected solver: ", this.selectedSolver);
    }
  },
};
</script>

<style scoped>
.navigation-buttons {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}

.back-button {
  margin-right: 1rem;
}

:deep(.custom-selector) {
  margin-top: 0.5rem;
  width: 100%;
}

.custom-label {
  margin-top: 1rem;
}

.optimize-button {
  margin-top: 1rem;
}

.p-invalid {
  border-color: var(--red-500) !important;
}
</style>
