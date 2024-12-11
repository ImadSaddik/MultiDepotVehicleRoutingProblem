<template>
  <div class="step-container">
    <h2>Data visualization</h2>

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
import Button from "primevue/button";

export default {
  name: "SidePanelStep2",
  components: {
    Button,
  },
  props: {},
  data() {
    return {};
  },
  methods: {
    goToNextStep() {
      this.$emit('next-step');
    },
    goToPreviousStep() {
      this.$emit('previous-step');
    },
  },
  watch: {},
};
</script>

<style scoped>
.step-container {
  padding: 1rem;
}

.navigation-buttons {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}

.back-button {
  margin-right: 1rem;
}
</style>
