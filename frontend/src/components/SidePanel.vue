<template>
  <div class="container">
    <TransitionGroup
      :name="animationDirection === 'forward' ? 'slide-left' : 'slide-right'" 
      mode="out-in"
    >
      <SidePanelStep1
        v-show="currentStep === 1"
        key="step1"
        @next-step="handleStep1Complete"
      />
      <SidePanelStep2
        v-show="currentStep === 2"
        key="step2"
        @next-step="handleNextStep"
        @previous-step="handlePreviousStep"
        @employee-slider-change="handleEmployeeSliderChange"
        @employee-toggle-switch-change="handleEmployeeToggleSwitchChange"
        @bus-slider-change="handleBusSliderChange"
        @bus-toggle-switch-change="handleBusToggleSwitchChange"
      />
      <SidePanelStep3
        v-show="currentStep === 3"
        key="step3"
        @next-step="handleNextStep"
        @previous-step="handlePreviousStep"
      />
    </TransitionGroup>
  </div>
</template>

<script>
import { dataStore } from "@/store/dataStore";

import SidePanelStep1 from "./SidePanelStep1.vue";
import SidePanelStep2 from "./SidePanelStep2.vue";
import SidePanelStep3 from "./SidePanelStep3.vue";

export default {
  name: "SidePanel",
  components: {
    SidePanelStep1,
    SidePanelStep2,
    SidePanelStep3
  },
  setup() {
    const store = dataStore()
    return { store }
  },
  data() {
    return {
      currentStep: 1,
      employeeData: [],
      busData: [],
      companyLocation: {},
      initialSliderValue: 5,
      animationDirection: 'forward',
    };
  },
  methods: {
    handleStep1Complete(data) {
      this.employeeData = data.employeeData;
      this.busData = data.busData;
      this.companyLocation = data.companyLocation;

      this.handleNextStep();
      this.sendSlicedData(this.initialSliderValue, this.initialSliderValue);
    },
    handleNextStep() {
      this.animationDirection = 'forward';
      this.currentStep++;
      this.store.setSidePanelStep(this.currentStep);
    },
    handlePreviousStep() {
      this.animationDirection = 'backward';
      this.currentStep--;
      this.store.setSidePanelStep(this.currentStep);
    },
    handleEmployeeSliderChange({ busValue, employeeValue }) {
      this.sendSlicedData(busValue, employeeValue);
    },
    handleBusSliderChange({ busValue, employeeValue }) {
      this.sendSlicedData(busValue, employeeValue);
    },
    sendSlicedData(busValue, employeeValue) {
      this.$emit("sliced-data", {
        employeeData: this.employeeData.slice(0, employeeValue),
        busData: this.busData.slice(0, busValue),
        companyData: this.store.companyData,
      });
    },
    handleEmployeeToggleSwitchChange(value) {
      this.$emit("employee-toggle-switch-change", value);
    },
    handleBusToggleSwitchChange(value) {
      this.$emit("bus-toggle-switch-change", value);
    },
  },
};
</script>

<style scoped>
.container {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 25rem;
  background-color: rgba(255, 255, 255, 0.95);
  border-left: 1px solid #adadad;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  overflow-y: auto;
}

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease;
  position: absolute;
  width: 100%;
}

.slide-left-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.slide-left-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-right-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
