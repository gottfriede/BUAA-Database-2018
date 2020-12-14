// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'

import axios from 'axios'
import Vuex from 'vuex'

Vue.use(Antd)
Vue.use(Vuex)
axios.defaults.withCredentials = true
Vue.prototype.$axios = axios

Vue.config.productionTip = false

const store = new Vuex.Store({
  state: {
    logged: false,
    userID: '',
    username: '',
    usertype: '',
    avatarSrc: ''
  },
  mutations: {
    changeUser (state, newValue) {
      state.username = newValue.username
      state.logged = true
      state.usertype = newValue.usertype
      state.userID = newValue.userID
      state.avatarSrc = newValue.avatarSrc
    },
    changeAvatar (state, newValue) {
      state.avatarSrc = newValue.avatarSrc
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
