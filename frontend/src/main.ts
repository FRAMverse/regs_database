import * as Vue from "vue";
import axios from "axios";
import dayjs from "dayjs";
import VueAxios from "vue-axios";
import App from "./App.vue";

import router from "./router";

import "./assets/main.css";

import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

const app = Vue.createApp(App);
app.config.globalProperties.$dayjs = dayjs;
app.use(router);
app.use(VueAxios, axios);

app.component('Datepicker', Datepicker);


app.mount("#app");
