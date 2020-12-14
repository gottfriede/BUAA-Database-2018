<template>
  <div class="register">
    <div id="sdeam-logo" style="text-align: center; margin: 20px">
      <img src="../assets/logo.png" alt="logo" width="400" height="135">
    </div>
    <a-form id="register-form" :form="form" @submit="handleSubmit" style="width: 74%; margin: 40px">
      <a-form-item v-bind="formItemLayout" label="用户名">
        <a-input
          v-decorator="[
            'userName',
            {
              rules: [
                {
                  required: true,
                  message: '请输入用户名',
                }
              ]
            }
          ]"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout" label="密码" has-feedback>
        <a-input-password
          v-decorator="[
            'password',
            {
              rules: [
                {
                  required: true,
                  message: '请输入密码',
                },
                {
                  validator: validateToNextPassword,
                },
              ],
            },
          ]"
          type="password"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout" label="确认密码" has-feedback>
        <a-input-password
          v-decorator="[
            'confirm',
            {
              rules: [
                {
                  required: true,
                  message: '请二次确认密码',
                },
                {
                  validator: compareToFirstPassword,
                },
              ],
            },
          ]"
          type="password"
          @blur="handleConfirmBlur"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout" label="用户类型">
        <a-cascader
          v-decorator="[
            'userType',
            {
              initialValue: ['individual'],
              rules: [
                { type: 'array', required: true, message: '请选择用户类型' },
              ],
            },
          ]"
          :options="usertypes"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout" label="电子邮箱">
        <a-input
          v-decorator="[
            'email'
          ]"
        />
      </a-form-item>
      <a-form-item v-bind="formItemLayout" label="电话">
        <a-input
          v-decorator="[
            'userTel'
          ]"
        />
      </a-form-item>
      <a-form-item v-bind="tailFormItemLayout">
        已经拥有SDEAM账号？
        <router-link to="/Login">
          <span>立即登录</span>
        </router-link>
      </a-form-item>
      <a-form-item v-bind="tailFormItemLayout">
        <a-button type="primary" html-type="submit" style="width: 100%">
          注册
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
const usertypes = [
  {
    value: 'individual',
    label: '个人'
  },
  {
    value: 'developer',
    label: '厂商'
  }
]

export default {
  data () {
    return {
      confirmDirty: false,
      usertypes,
      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 8 }
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 16 }
        }
      },
      tailFormItemLayout: {
        wrapperCol: {
          xs: {
            span: 24,
            offset: 0
          },
          sm: {
            span: 16,
            offset: 8
          }
        }
      }
    }
  },
  beforeCreate () {
    this.form = this.$form.createForm(this, { name: 'register' })
  },
  methods: {
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          if (values.userType[0] === 'individual') {
            console.log('true')
            this.$axios.post('http://127.0.0.1:5000/userRegister', {
              'userName': values.userName,
              'password': values.password,
              'email': values.email,
              'userTel': values.userTel
            }).then((response) => {
              this.$notification['success']({
                message: '注册成功',
                description: ''
              })
              this.$router.push('login')
            }).catch((e) => {
              this.$notification['error']({
                message: '注册失败',
                description: '用户名已被占用'
              })
            })
          } else {
            console.log('false')
            this.$axios.post('http://127.0.0.1:5000/developerRegister', {
              'developerName': values.userName,
              'password': values.password,
              'email': values.email,
              'developerTel': values.userTel
            }).then((response) => {
              this.$notification['success']({
                message: '注册成功',
                description: ''
              })
              this.$router.push('login')
            }).catch((e) => {
              this.$notification['error']({
                message: '注册失败',
                description: '用户名已被占用'
              })
            })
          }
        }
      })
    },
    handleConfirmBlur (e) {
      const value = e.target.value
      this.confirmDirty = this.confirmDirty || !!value
    },
    compareToFirstPassword (rule, value, callback) {
      const form = this.form
      if (value && value !== form.getFieldValue('password')) {
        callback(new Error('请再次输入相同的密码'))
      } else {
        callback()
      }
    },
    validateToNextPassword (rule, value, callback) {
      const form = this.form
      if (value && this.confirmDirty) {
        form.validateFields(['confirm'], { force: true })
      }
      callback()
    }
  }
}
</script>

<style scoped>
</style>
