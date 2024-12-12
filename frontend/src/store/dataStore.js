import { defineStore } from "pinia";

export const dataStore = defineStore("data", {
  state: () => ({
    employeeData: [],
    busData: [],
    companyData: {},
    sidePanelStep: 1,
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
  },
});
