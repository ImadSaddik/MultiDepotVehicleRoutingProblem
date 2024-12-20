import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import PrimeVue from "primevue/config";
import Tooltip from 'primevue/tooltip';
import Aura from "@primevue/themes/aura"
import ToastService from 'primevue/toastservice';
import axios from "axios";
import 'primeicons/primeicons.css'

axios.defaults.baseURL = 'http://localhost:8000'
const app = createApp(App);
app.use(createPinia())
app.use(router, axios);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: '.my-app-dark',
            cssLayer: false
        }
    }
});
app.use(ToastService);
app.directive('tooltip', Tooltip);
app.mount("#app");
