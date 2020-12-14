<template>
  <div id="login">
    <div id="sdeam-logo" style="text-align: center; margin-top: 100px">
      <img src="../assets/logo.png" alt="logo" width="400" height="135">
    </div>
    <a-form
      id="login-form"
      :form="form"
      class="login-form"
      @submit="handleSubmit"
      style="margin-left: 37%; margin-right: 37%; margin-top: 40px;"
    >
      <a-form-item>
        <a-input
          v-decorator="[
            'username',
            { rules: [{ required: true, message: '请输入用户名' }] },
          ]"
          placeholder="Username"
        >
          <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)" />
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-input-password
          v-decorator="[
            'password',
            { rules: [{ required: true, message: '请输入密码' }] },
          ]"
          type="password"
          placeholder="Password"
        >
          <a-icon slot="prefix" type="lock" style="color: rgba(0,0,0,.25)" />
        </a-input-password>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit" class="login-form-button">
          <span v-if="!isUser">
            开发者账号
          </span>
          登录
        </a-button>
        还没有账号？
        <router-link to="/Register">
          <span>立即注册</span>
        </router-link>
        <span v-if="isUser">
          <br>
          已成为开发者？
          <a @click="() => changeUserType()">使用开发者账号登录</a>
        </span>
        <span v-if="!isUser">
          <br>
          没有成为开发者？
          <a @click="() => changeUserType()">使用用户账号登录</a>
        </span>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      isUser: true,
      isAdmin: false
    }
  },
  beforeCreate () {
    this.form = this.$form.createForm(this, { name: 'normal_login' })
  },
  methods: {
    changeUserType () {
      this.isUser = !this.isUser
    },
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          if (this.isUser) {
            console.log('Received values of form: ', values)
            this.$axios.post('http://127.0.0.1:5000/userLogin', {
              'userName': values.username,
              'userPassword': values.password
            }).then((response) => {
              console.log(response.data)
              this.$axios.post('http://127.0.0.1:5000/getUserTable', {
                'userID': response.data.userID
              }).then((res) => {
                this.$store.commit('changeUser', {
                  'username': values.username,
                  'usertype': 'individual',
                  'userID': response.data.userID,
                  'avatarSrc': res.data.userGraph
                })
                this.$notification['success']({
                  message: '登录成功'
                })
                this.$router.push('store')
              })
            }).catch((e) => {
              this.$notification['error']({
                message: '登陆失败',
                description: '用户名或密码错误'
              })
            })
          } else {
            console.log('Received values of form: ', values)
            this.$axios.post('http://127.0.0.1:5000/developerLogin', {
              'developerName': values.username,
              'developerPassword': values.password
            }).then((response) => {
              console.log(response.data)
              this.$axios.post('http://127.0.0.1:5000/queryDeveloper', {
                'developerID': response.data.developerID
              }).then((res) => {
                this.$store.commit('changeUser', {
                  'username': values.username,
                  'usertype': 'developer',
                  'userID': response.data.developerID,
                  'avatarSrc': res.data.developerGraph
                })
                this.$notification['success']({
                  message: '登录成功'
                })
                this.$router.push('store')
              })
            }).catch((e) => {
              this.$notification['error']({
                message: '登陆失败',
                description: '用户名或密码错误'
              })
            })
          }
        }
      })
    }
  }
}
</script>

<style scoped>
#login-form .login-form {
  max-width: 300px;
}
#login-form .login-form-forgot {
  float: right;
}
#login-form .login-form-button {
  width: 100%;
}
</style>
