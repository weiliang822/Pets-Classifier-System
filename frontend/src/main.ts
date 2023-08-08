import { createApp } from 'vue'
import App from './App.vue'
import router from "./router"
// import VueAxios from 'vue-axios'
import axios from 'axios'

import { library } from "@fortawesome/fontawesome-svg-core";
import { faWeixin, faQq, faWeibo, faAlipay } from "@fortawesome/free-brands-svg-icons";
import { faUser, faLock, faEnvelope } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import screenfull from "screenfull";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

library.add(faWeixin, faQq, faWeibo, faAlipay, faUser, faLock, faEnvelope);

const app = createApp(App)
app.component("font-awesome-icon", FontAwesomeIcon)
app.use(router)
app.use(ElementPlus)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
