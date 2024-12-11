<template>
  <div class="container">
    <SidePanelStep1
      v-show="currentStep === 1"
      @next-step="handleStep1Complete"
    />
    <SidePanelStep2
      v-show="currentStep === 2"
      @next-step="handleNextStep"
      @previous-step="handlePreviousStep"
    />
  </div>
</template>

<script>
import SidePanelStep1 from "./SidePanelStep1.vue";
import SidePanelStep2 from "./SidePanelStep2.vue";

export default {
  name: "SidePanel",
  components: {
    SidePanelStep1,
    SidePanelStep2,
  },
  data() {
    return {
      currentStep: 1,
      employeeData: [],
      busData: [],
      companyLocation: {},
    };
  },
  methods: {
    handleStep1Complete(data) {
      this.employeeData = data.employeeData;
      this.busData = data.busData;
      this.companyLocation = data.companyLocation;
      this.currentStep++;
    },
    handleNextStep() {
      this.currentStep++;
    },
    handlePreviousStep() {
      this.currentStep--;
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
</style>
