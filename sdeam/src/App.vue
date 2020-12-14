<template>
  <div id="app">
    <a-layout id="components-layout-demo-side" style="min-height: 100vh">
    <a-layout-sider v-model="collapsed" collapsible>
      <div class="logo"/>
      <a-menu theme="dark" :default-selected-keys="['1']" mode="inline">
        <a-menu-item key="1">
          <a-icon type="shop" />
          <span>商店</span>
          <router-link to="/Store" ></router-link>
        </a-menu-item>
        <a-menu-item key="2">
          <a-icon type="appstore" />
          <span>库</span>
          <router-link to="/Library" ></router-link>
        </a-menu-item>
        <a-menu-item key="3" v-if="this.$store.state.usertype === 'individual'">
          <a-icon type="menu" />
          <span>愿望单</span>
          <router-link to="/WishList" ></router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0">
        <a-row>
          <a-col :span="12">
            <img src="./assets/logo.png" alt="logo" width="145" height="50" >
          </a-col>
          <a-col :span="12">
            <div id='userInfo' style="text-align: right; margin-right: 20px;">
              <div v-show="this.$store.state.logged == true">
                <a-avatar :src="this.$store.state.avatarSrc" width="50" height="50" v-if="this.$store.state.usertype !== 'admin'"/>
                <span>{{this.$store.state.username}}</span>
                <a-dropdown :trigger="['click']">
                  <a class="dropdown-menu" @click="e => e.preventDefault()">
                    <a-icon type="down" />
                  </a>
                  <a-menu slot="overlay">
                    <a-menu-item>
                      <div @click="changeToUser()" v-if="this.$store.state.usertype !== 'admin'" >
                        <a-icon type="user" />
                        <span>个人中心</span>
                      </div>
                    </a-menu-item>
                    <a-menu-item>
                      <div @click="logout()">
                        <a-icon type="poweroff" />
                        <span>注销</span>
                      </div>
                    </a-menu-item>
                  </a-menu>
                </a-dropdown>
              </div>
              <div v-show="this.$store.state.logged == false">
                <router-link to="/AdminLogin" >
                  <span>管理员入口</span>
                </router-link>
                <a-divider type="vertical" />
                <router-link to="/Login" >
                  <span>登录</span>
                </router-link>
                <a-divider type="vertical" />
                <router-link to="/Register" >
                  <span>注册</span>
                </router-link>
              </div>
            </div>
          </a-col>
        </a-row>
      </a-layout-header>
      <a-layout-content style="margin: 0 16px">

        <router-view />

      </a-layout-content>
      <a-layout-footer style="text-align: center">
        SDEAM ©2020 Created by Gottfried
      </a-layout-footer>
    </a-layout>
  </a-layout>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      collapsed: false
    }
  },
  methods: {
    logout () {
      this.$store.state.logged = false
      this.$store.state.username = ''
      this.$store.state.usertype = ''
      this.$store.state.userID = ''
      this.$store.state.avatarSrc = ''
      this.$notification['success']({
        message: '注销成功'
      })
      this.$router.push('/Login')
    },
    changeToUser () {
      if (this.$store.state.usertype === 'individual') {
        this.$router.push('/User/1/' + this.$store.state.userID)
      } else if (this.$store.state.usertype === 'developer') {
        this.$router.push('/User/2/' + this.$store.state.userID)
      }
    }
  },
  created () {
    this.$router.push('login')
  }
}
</script>

<style>
#components-layout-demo-side .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}

#userInfo {
  margin: 0px;
}
</style>
