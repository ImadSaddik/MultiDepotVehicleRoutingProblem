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
      :loading="isSolving"
      label="Optimize"
      iconPos="right"
      class="optimize-button"
      @click="startSolver"
    />

    <Transition name="fade">
      <ProgressBar
        :value="optimizationProgress"
        class="progress-bar"
        v-if="isSolving"
      />
    </Transition>
    <Transition name="fade">
      <div
        v-show="isSolving || (optimizationDuration && !isResultAvailable)"
        class="timer"
      >
        {{ formattedDuration }}
      </div>
    </Transition>
    <Transition name="fade">
      <div
        v-if="!isSolving && optimizationDuration && isResultAvailable"
        class="completion-message"
      >
        The optimization took {{ formattedDuration }}
      </div>
    </Transition>

    <Toast position="bottom-left" />

    <div class="navigation-buttons">
      <Button
        label="Back"
        icon="pi pi-arrow-left"
        class="back-button"
        @click="goToPreviousStep"
      />
      <Button
        :disabled="isSolving"
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
import ProgressBar from "primevue/progressbar";

import axios from "axios";

export default {
  name: "SidePanelStep3",
  components: {
    Toast,
    Button,
    Select,
    Divider,
    ProgressBar,
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
      isSolving: false,
      isResultAvailable: false,
      isSolverInvalid: false,
      optimizationProgress: 0,
      POLLING_DURATION_MS: 100,
      COMPLETION_PERCENTAGE: 100,
      TOAST_DURATION: 5000,
      optimizationDuration: 0,
      timerInterval: null,
    };
  },
  computed: {
    formattedDuration() {
      const hours = String(
        Math.floor(this.optimizationDuration / 3600)
      ).padStart(2, "0");
      const minutes = String(
        Math.floor((this.optimizationDuration % 3600) / 60)
      ).padStart(2, "0");
      const seconds = String(this.optimizationDuration % 60).padStart(2, "0");
      return `${hours}:${minutes}:${seconds}`;
    },
  },
  methods: {
    goToNextStep() {
      if (!this.selectedSolver) {
        this.isSolverInvalid = true;
        this.$toast.add({
          severity: "error",
          summary: "Validation error",
          detail: "Please select a solver",
          life: this.TOAST_DURATION,
        });
        return;
      }

      this.isSolverInvalid = false;
      this.$emit("next-step");
    },
    goToPreviousStep() {
      this.$emit("previous-step");
    },
    async startSolver() {
      if (!this.selectedSolver) {
        this.isSolverInvalid = true;
        this.$toast.add({
          severity: "error",
          summary: "Validation error",
          detail: "Please select a solver",
          life: this.TOAST_DURATION,
        });
        return;
      }
      this.optimizationDuration = 0;
      this.isResultAvailable = false;
      this.isSolverInvalid = false;
      this.isSolving = true;
      this.startTimer();

      await this.resetOptimizationProgress();
      this.fetchOptimizationProgress();

      const endpointUrl = `${axios.defaults.baseURL}/api/v1/optimize?solver_method=${this.selectedSolver["value"]}`;
      await axios
        .post(endpointUrl)
        .then((response) => {
          this.store.setOptimizedData(response.data.data);
          this.isResultAvailable = true;
          this.isSolving = false;
          this.stopTimer();

          this.$toast.add({
            severity: "success",
            summary: "Optimization success",
            detail: "The routes have been optimized",
            life: this.TOAST_DURATION,
          });
        })
        .catch((error) => {
          this.isResultAvailable = false;
          this.isSolving = false;
          this.stopTimer();

          this.$toast.add({
            severity: "error",
            summary: "Optimization error",
            detail: error.response.data.message,
            life: this.TOAST_DURATION,
          });
        });
    },
    startTimer() {
      this.timerInterval = setInterval(() => {
        this.optimizationDuration++;
      }, 1000);
    },
    stopTimer() {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    },
    async fetchOptimizationProgress() {
      try {
        const endpointUrl = `${axios.defaults.baseURL}/api/v1/optimize/progress/`;
        const response = await axios.get(endpointUrl);

        this.optimizationProgress = response.data.progress;

        if (this.optimizationProgress < this.COMPLETION_PERCENTAGE) {
          setTimeout(this.fetchOptimizationProgress, this.POLLING_DURATION_MS);
        } else {
          this.isSolving = false;
        }
      } catch (error) {
        this.$toast.add({
          severity: "error",
          summary: "Progress error",
          detail: error.response.data.message,
          life: this.TOAST_DURATION,
        });
      }
    },
    async resetOptimizationProgress() {
      await axios
        .post(`${axios.defaults.baseURL}/api/v1/optimize/reset-progress/`)
        .then(() => {})
        .catch((error) => {
          console.error("Error resetting progress", error);
          this.isSolving = false;
        });
    },
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
  width: 100%;
}

.p-invalid {
  border-color: var(--red-500) !important;
}

.progress-bar {
  margin-top: 1rem;
  height: 1.5rem;
}

.timer {
  margin-top: 1rem;
}

.completion-message {
  margin-top: 1rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
