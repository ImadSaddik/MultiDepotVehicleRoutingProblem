import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import PrimeVue from "primevue/config";
import Tooltip from 'primevue/tooltip';
import Aura from "@primevue/themes/aura"
import 'primeicons/primeicons.css'
import ToastService from 'primevue/toastservice';

const app = createApp(App);
app.use(createPinia())
app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'light',
            cssLayer: false
        }
    }
});
app.use(ToastService);
app.directive('tooltip', Tooltip);
app.mount("#app");
