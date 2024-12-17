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

      <p>Bus N° {{ selectedCluster + 1 }}</p>

      <Button 
        :disabled="selectedCluster === store.optimizedData.length - 1"
        icon="pi pi-chevron-right"
        class="toggle-button" 
        @click="showNextCluster" 
      />
    </div>

    <div class="segment-controls">
      <p style="margin: 0px;">
        The route is divided into segments. You can view the full route or view each segment individually.
      </p>
      
      <div class="segment-mode-toggle">
        <ToggleButton
          v-model="showFullRoute"
          onLabel="Full route"
          offLabel="Segment view"
          class="w-full"
        />
      </div>

      <div v-if="!showFullRoute" class="segment-navigation">
        <Button 
          :disabled="selectedSegment === 0"
          icon="pi pi-chevron-left"
          class="toggle-button"
          @click="showPreviousSegment" 
        />

        <p>Segment {{ selectedSegment + 1 }} of {{ totalSegments }}</p>

        <Button 
          :disabled="selectedSegment === totalSegments - 1"
          icon="pi pi-chevron-right"
          class="toggle-button" 
          @click="showNextSegment" 
        />
      </div>
    </div>

    <Divider class="custom-divider" />

    <h2>Route statistics</h2>
    <div class="statistics-container">
      <Card class="stat-card">
        <template #header>
          <div class="card-header">
            <i class="pi pi-map-marker" style="font-size: 2rem"></i>
            <h3>Total distance</h3>
          </div>
        </template>
        <template #content>
          <div class="stat-content">
            <div class="stat-number">{{ formatDistance }}</div>
            <div class="stat-label">kilometers</div>
          </div>
        </template>
      </Card>

      <Card class="stat-card">
        <template #header>
          <div class="card-header">
            <i class="pi pi-clock" style="font-size: 2rem"></i>
            <h3>Duration</h3>
          </div>
        </template>
        <template #content>
          <div class="stat-content">
            <div class="stat-number">{{ formatDuration }}</div>
            <div class="stat-label">minutes</div>
          </div>
        </template>
      </Card>

      <Card class="stat-card">
        <template #header>
          <div class="card-header">
            <i class="pi pi-users" style="font-size: 2rem"></i>
            <h3>Passengers</h3>
          </div>
        </template>
        <template #content>
          <div class="stat-content">
            <div class="stat-number">{{ passengerCount }}</div>
            <div class="stat-label">employees</div>
          </div>
        </template>
      </Card>
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
import { toRaw } from "vue";
import { dataStore } from "@/store/dataStore";

import Card from 'primevue/card';
import Toast from "primevue/toast";
import Button from "primevue/button";
import Divider from 'primevue/divider';
import ToggleButton from 'primevue/togglebutton';

export default {
  name: "SidePanelStep4",
  components: {
    Card,
    Toast,
    Button,
    Divider,
    ToggleButton,
  },
  setup() {
    const store = dataStore();
    return { store };
  },
  data() {
    return {
      selectedCluster: 0,
      selectedSegment: 0,
      showFullRoute: true,
    };
  },
  watch: {
    selectedCluster() {
      this.$emit("cluster-selected", this.getClusterData());
    },
    "store.sidePanelStep"(val) {
      if (val === 4) {
        this.$emit("cluster-selected", this.getClusterData());
      }
    },
    showFullRoute() {
      this.$emit("cluster-selected", this.getClusterData());
    },
    selectedSegment() {
      this.$emit("cluster-selected", this.getClusterData());
    },
  },
  computed: {
    currentClusterData() {
      return this.store.optimizedData[this.selectedCluster];
    },
    formatDistance() {
      const distanceInMeters = this.currentClusterData?.total_distance || 0;
      return (distanceInMeters / 1000).toFixed(3);
    },
    formatDuration() {
      const seconds = this.currentClusterData?.total_duration || 0;
      return Math.round(seconds / 60);
    },
    passengerCount() {
      return this.currentClusterData?.employee_nodes?.length || 0;
    },
    totalSegments() {
      return this.currentClusterData?.route_segments?.length || 0;
    },
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
      this.store.setSelectedCluster(this.selectedCluster);
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
      this.store.setSelectedCluster(this.selectedCluster);
    },
    showNextSegment() {
      if (this.selectedSegment < this.totalSegments - 1) {
        this.selectedSegment++;
      }
    },
    showPreviousSegment() {
      if (this.selectedSegment > 0) {
        this.selectedSegment--;
      }
    },
    getClusterData() {
      const clusterData = toRaw(this.store.optimizedData[this.selectedCluster]);
      return {
        busData: [clusterData["bus_node"]],
        employeeData: clusterData["employee_nodes"],
        companyData: clusterData["company_node"],
        routeDisplayMode: {
          showFullRoute: this.showFullRoute,
          selectedSegment: this.selectedSegment,
        },
      };
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

.statistics-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
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

.segment-controls {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
}

.segment-mode-toggle {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.segment-navigation {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.p-togglebutton) {
  width: 100%;
}

:deep(.p-togglebutton.p-highlight) {
  background: var(--primary-color);
  border-color: var(--primary-color);
}
</style>
