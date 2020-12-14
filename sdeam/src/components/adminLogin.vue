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
          管理员登录
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data () {
    return {
    }
  },
  beforeCreate () {
    this.form = this.$form.createForm(this, { name: 'normal_login' })
  },
  methods: {
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.$axios.post('http://127.0.0.1:5000/adminLogin', {
            'adminCount': values.username,
            'adminPassword': values.password
          }).then((response) => {
            console.log(response.data)
            this.$store.commit('changeUser', {
              'username': 'admin',
              'usertype': 'admin',
              'userID': response.data.adminID
            })
            this.$notification['success']({
              message: '欢迎'
            })
            this.$router.push('/Store')
          }).catch((e) => {
            this.$notification['error']({
              message: '登陆失败',
              description: '用户名或密码错误'
            })
          })
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
