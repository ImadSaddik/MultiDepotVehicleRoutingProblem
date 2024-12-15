import { defineStore } from "pinia";

export const dataStore = defineStore("data", {
  state: () => ({
    employeeData: [],
    busData: [],
    companyData: {},
    sidePanelStep: 1,
    optimizedData: [],
    selectedCluster: null,
  }),
  actions: {
    setEmployeeData(data) {
      this.employeeData = data;
    },
    setBusData(data) {
      this.busData = data;
    },
    setCompanyData(data) {
      this.companyData = data;
    },
    setSidePanelStep(step) {
      this.sidePanelStep = step;
    },
    setOptimizedData(data) {
      this.optimizedData = data;
    },
    setSelectedCluster(cluster) {
      this.selectedCluster = cluster;
    },
  },
});
