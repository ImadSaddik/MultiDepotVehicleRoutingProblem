<template>
  <div class="step-container">
    <h1>Routing solver</h1>
    <h2>Data visualization</h2>

    <p>
      This is the second step of the routing solver. Here you can visualize the
      data you uploaded to verify that it is correct before proceeding to the
      next step.
    </p>

    <div class="data-slider-container">
      <p>Employee data</p>
      <div class="toggle-switch-container">
        <ToggleSwitch
          v-model="employeeToggleSwitchChecked"
          @update:modelValue="handleEmployeeToggleSwitchChange"
        />
        <span v-if="employeeToggleSwitchChecked">
          Displaying {{ employeeSliderValue }} employee records
        </span>
        <span v-else> Enable to view employee records </span>
      </div>
      <div class="slider-with-labels">
        <span class="slider-label">1</span>
        <Slider
          v-model="employeeSliderValue"
          :min="1"
          :max="maxEmployeeSliderValue"
          :disabled="!employeeToggleSwitchChecked"
          @update:modelValue="handleEmployeeSliderChange"
        />
        <span class="slider-label">{{ maxEmployeeSliderValue }}</span>
      </div>
    </div>

    <div class="data-slider-container">
      <p>Bus data</p>
      <div class="toggle-switch-container">
        <ToggleSwitch
          v-model="busToggleSwitchChecked"
          @update:modelValue="handleBusToggleSwitchChange"
        />
        <span v-if="busToggleSwitchChecked">
          Displaying {{ busSliderValue }} bus records
        </span>
        <span v-else> Enable to view bus records </span>
      </div>
      <div class="slider-with-labels">
        <span class="slider-label">1</span>
        <Slider
          v-model="busSliderValue"
          :min="1"
          :max="maxBusSliderValue"
          :disabled="!busToggleSwitchChecked"
          @update:modelValue="handleBusSliderChange"
        />
        <span class="slider-label">{{ maxBusSliderValue }}</span>
      </div>
    </div>

    <Divider class="custom-divider" />

    <h2>Statistics</h2>
    <p>Here you can see some statistics about the data you uploaded.</p>

    <div class="statistics-container">
      <Card class="stat-card">
        <template #header>
          <div class="card-header">
            <i class="pi pi-users" style="font-size: 2rem"></i>
            <h3>Employees</h3>
          </div>
        </template>
        <template #content>
          <div class="stat-content">
            <div class="stat-number">{{ totalEmployees }}</div>
            <div class="stat-label">Total records</div>
          </div>
        </template>
      </Card>

      <Card class="stat-card">
        <template #header>
          <div class="card-header">
            <i class="pi pi-truck" style="font-size: 2rem"></i>
            <h3>Buses</h3>
          </div>
        </template>
        <template #content>
          <div class="stat-content">
            <div class="stat-number">{{ totalBuses }}</div>
            <div class="stat-label">Total records</div>
          </div>
        </template>
      </Card>
    </div>

    <div class="navigation-buttons">
      <Button
        label="Back"
        icon="pi pi-arrow-left"
        class="back-button"
        @click="goToPreviousStep"
      />
      <Button
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

import Button from "primevue/button";
import Slider from "primevue/slider";
import Divider from "primevue/divider";
import ToggleSwitch from "primevue/toggleswitch";
import Card from "primevue/card";

export default {
  name: "SidePanelStep2",
  components: {
    Button,
    Slider,
    Divider,
    ToggleSwitch,
    Card,
  },
  setup() {
    const store = dataStore();
    return { store };
  },
  computed: {
    maxEmployeeSliderValue() {
      let employeeDataSize = this.store.employeeData.length;
      return Math.min(employeeDataSize, this.maxValueForSlider);
    },
    maxBusSliderValue() {
      let busDataSize = this.store.busData.length;
      return Math.min(busDataSize, this.maxValueForSlider);
    },
    totalEmployees() {
      return this.store.employeeData.length;
    },
    totalBuses() {
      return this.store.busData.length;
    },
  },
  data() {
    return {
      employeeToggleSwitchChecked: true,
      employeeSliderValue: 5,
      busToggleSwitchChecked: true,
      busSliderValue: 5,
      maxValueForSlider: 50,
    };
  },
  methods: {
    goToNextStep() {
      this.$emit("next-step");
    },
    goToPreviousStep() {
      this.$emit("previous-step");
    },
    handleEmployeeSliderChange(currentEmployeeSliderValue) {
      this.$emit("employee-slider-change", {
        busValue: this.busSliderValue,
        employeeValue: currentEmployeeSliderValue,
      });
    },
    handleBusSliderChange(currentBusSliderValue) {
      this.$emit("bus-slider-change", {
        busValue: currentBusSliderValue,
        employeeValue: this.employeeSliderValue,
      });
    },
    handleEmployeeToggleSwitchChange(value) {
      this.$emit("employee-toggle-switch-change", value);
    },
    handleBusToggleSwitchChange(value) {
      this.$emit("bus-toggle-switch-change", value);
    },
  },
  watch: {},
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

.data-slider-container {
  margin-top: 2rem;
}

.toggle-switch-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.slider-with-labels {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

:deep(.p-slider) {
  flex: 1;
}

.statistics-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
}

.card-header h3 {
  margin: 0;
  color: var(--primary-color);
  font-size: 1.2rem;
}

.card-header i {
  font-size: 1.2rem !important;
}

.stat-content {
  text-align: center;
  padding: 0.5rem;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: bold;
  line-height: 1;
}

.stat-label {
  margin-top: 0.25rem;
  font-size: 0.9rem;
}

:deep(.p-card) {
  border-radius: 0.5rem;
}
</style>
