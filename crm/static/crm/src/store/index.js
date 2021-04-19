import Vue from 'vue'
import Vuex from 'vuex'

import Alert from './Alert'
import User from './User'
import Page from './Page'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    User,
    Alert,
    Page
  },
  strict: process.env.NODE_ENV !== 'production',
  state: {
    count: 1
  },
  mutations: {
    increment(state, payload) {
      state.count += payload.counter
    }
  }
})

export default store
