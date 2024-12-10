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
    <div v-if="employeeData.length > 0" class="data-visualize-icon">
      <Button
        icon="pi pi-table"
        class="p-button-text"
        @click="showEmployeeDialog = true"
        label="View employee data"
        raised
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
    <div v-if="busData.length > 0" class="data-visualize-icon">
      <Button
        icon="pi pi-table"
        class="p-button-text"
        @click="showBusDialog = true"
        label="View Bus Data"
        raised
      />
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

    <Dialog
      header="Employee data"
      v-model:visible="showEmployeeDialog"
      maximizable
      :modal="true"
      :draggable="false"
      :resizable="false"
      :transitionOptions="{ transition: 'fade' }"
    >
      <DataTable
        showGridlines
        stripedRows
        paginator
        :rows="10"
        scrollable
        scrollHeight="flex"
        :value="employeeData"
        :size="large"
        :rowsPerPageOptions="[10, 20, 50]"
        tableStyle="min-width: 50rem"
      >
        <Column field="ID" header="ID"></Column>
        <Column field="Latitude" header="Latitude"></Column>
        <Column field="Longitude" header="Longitude"></Column>
      </DataTable>
    </Dialog>

    <Dialog
      header="Bus data"
      v-model:visible="showBusDialog"
      maximizable
      :modal="true"
      :draggable="false"
      :resizable="false"
      :transitionOptions="{ transition: 'fade' }"
    >
      <DataTable
        showGridlines
        stripedRows
        paginator
        :rows="10"
        scrollable
        scrollHeight="flex"
        :value="busData"
        :size="large"
        :rowsPerPageOptions="[10, 20, 50]"
        tableStyle="min-width: 50rem"
      >
        <Column field="ID" header="ID"></Column>
        <Column field="Latitude" header="Latitude"></Column>
        <Column field="Longitude" header="Longitude"></Column>
      </DataTable>
    </Dialog>
  </div>
</template>

<script>
import FileUpload from "primevue/fileupload";
import InputNumber from "primevue/inputnumber";
import Divider from "primevue/divider";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import * as XLSX from "xlsx";

export default {
  name: "SidePanel",
  components: {
    FileUpload,
    InputNumber,
    Button,
    Divider,
    Dialog,
    DataTable,
    Column,
  },
  data() {
    return {
      companyLatitude: null,
      companyLongitude: null,
      employeeData: [],
      busData: [],
      showEmployeeDialog: false,
      showBusDialog: false,
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

        const normalizedData = jsonData.map((item) => ({
          ID: item.id,
          Latitude: item.lat,
          Longitude: item.lon,
        }));
        this[dataProperty] = normalizedData;
      };
      reader.readAsArrayBuffer(file);
    },
    onEmployeeUpload(event) {
      this.handleFileUpload(event, "employeeData");
    },
    onBusUpload(event) {
      this.handleFileUpload(event, "busData");
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

.data-visualize-icon {
  margin-top: 0.5rem;
}
</style>
