import Vue from 'vue'
import CihubApi from './plugins/CihubApi.js'
import App from './App.vue'

Vue.config.productionTip = false
Vue.use(CihubApi);

const VueInstance = new Vue({
  render: h => h(App),
}).$mount('#app');

export default VueInstance
