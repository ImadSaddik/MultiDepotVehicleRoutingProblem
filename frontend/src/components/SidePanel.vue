<template>
  <div class="container">
    <h1>Routing solver</h1>
    <h2>Employee and bus coordinates</h2>

    <div class="employees-file-upload">
      <label for="employeeFile">Employee File:</label>
      <FileUpload
        id="employeeFile"
        name="employeeFile"
        mode="basic"
        accept=".csv,.xlsx"
        :maxFileSize="5000000"
        @select="onEmployeeUpload"
      />
    </div>

    <div class="bus-file-upload">
      <label for="busFile">Bus File:</label>
      <FileUpload
        id="busFile"
        name="busFile"
        mode="basic"
        accept=".csv,.xlsx"
        :maxFileSize="5000000"
        @select="onBusUpload"
      >
        <template #empty>
          <span>Drag and drop the bus file here to upload.</span>
        </template>
      </FileUpload>
    </div>

    <p>
      <b>Note</b>: Please upload the employee and bus location files (in CSV or
      Excel format). Each file should include three columns: <b>ID</b>,
      <b>Latitude</b>, and <b>Longitude</b>.
    </p>

    <Divider class="custom-divider" />

    <h2>Company location</h2>

    <div class="latitude-input-container">
      <label for="companyLatitude">Latitude:</label>
      <InputNumber
        fluid
        v-model="companyLatitude"
        placeholder="Latitude"
        useGrouping="false"
        inputId="companyLatitude"
        suffix="°"
        :mode="'decimal'"
        :minFractionDigits="0"
        :maxFractionDigits="10"
        :min="-90"
        :max="90"
      />
    </div>
    <div class="longitude-input-container">
      <label for="companyLongitude">Longitude:</label>
      <InputNumber
        fluid
        v-model="companyLongitude"
        placeholder="Longitude"
        useGrouping="false"
        suffix="°"
        :mode="'decimal'"
        :minFractionDigits="0"
        :maxFractionDigits="10"
        :min="-180"
        :max="180"
      />
    </div>

    <Button
      label="Next"
      icon="pi pi-arrow-right"
      class="next-button"
      @click="goToNextStep"
    />
  </div>
</template>

<script>
import FileUpload from "primevue/fileupload";
import InputNumber from "primevue/inputnumber";
import Divider from 'primevue/divider';
import Button from "primevue/button";
import * as XLSX from "xlsx";

export default {
  name: "SidePanel",
  components: {
    FileUpload,
    InputNumber,
    Button,
    Divider,
  },
  data() {
    return {
      companyLatitude: null,
      companyLongitude: null,
      employeeData: [],
      busData: [],
    };
  },
  methods: {
    handleFileUpload(event, dataProperty) {
      const file = event.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(firstSheet);
        this[dataProperty] = jsonData;
      };
      reader.readAsArrayBuffer(file);
    },
    onEmployeeUpload(event) {
      this.handleFileUpload(event, 'employeeData');
    },
    onBusUpload(event) {
      this.handleFileUpload(event, 'busData');
    },
    goToNextStep() {
      // Implement navigation to the next step
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
  padding: 1rem;
}

.employees-file-upload,
.bus-file-upload,
.latitude-input-container,
.longitude-input-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

.next-button {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}

.custom-divider {
  width: 60%;
  margin: 1rem auto;
}
</style>
