import '@babel/polyfill'
import 'mutationobserver-shim'
import './plugins/bootstrap-vue'
import './plugins/axios'
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
