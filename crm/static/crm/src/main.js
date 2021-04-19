import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import vuetify from '@/plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.config.productionTip = false
Vue.config.devtools = true

store.dispatch('User/load')

/* eslint-disable no-new */
new Vue({
  el: '#root',
  router,
  vuetify,
  store,
  template: '<App/>',
  components: {App}
})
