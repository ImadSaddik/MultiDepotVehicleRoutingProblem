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
        <ToggleSwitch v-model="employeeToggleSwitchChecked" @update:modelValue="handleEmployeeToggleSwitchChange" />
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
        <ToggleSwitch v-model="busToggleSwitchChecked" @update:modelValue="handleBusToggleSwitchChange" />
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

export default {
  name: "SidePanelStep2",
  components: {
    Button,
    Slider,
    Divider,
    ToggleSwitch,
  },
  setup() {
    const store = dataStore()
    return { store }
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
    }
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
</style>
