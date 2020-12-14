<template>
  <div class="User">
    <div v-show="this.$store.state.logged == false">
      <router-link to="/Login">
        <span>登录</span>
      </router-link>
      <span>或</span>
      <router-link to="/Register">
        <span>立即注册</span>
      </router-link>
    </div>
    <div v-show="this.$store.state.logged == true">
      <a-row>
        <a-col :span="6">
          <div style="text-align: right; margin-top: 150px">
            <a-avatar :src="avatarSrc" :size="128"/>
            <div style="margin-left: 310px; margin-top: 50px">
                <a-upload
                  name="userGraph"
                  list-type="picture-card"
                  class="avatar-uploader"
                  :show-upload-list="false"
                  action="http://127.0.0.1:5000/uploadUserGraph"
                  :on-success="onSuccess"
                  :before-upload="beforeUpload"
                  @change="handleChange"
                >
                  <img v-if="imageUrl" :src="imageUrl" width="110" height="110" alt="avatar" />
                  <div v-else>
                    <a-icon :type="loading ? 'loading' : 'plus'" />
                    <div class="ant-upload-text">
                      上传新头像
                    </div>
                  </div>
                </a-upload>
            </div>
          </div>
        </a-col>
        <a-col :span="18">
          <a-form :form="form" @submit="handleSubmit" style="width: 50%; margin-top: 100px;">
        <a-form-item v-bind="formItemLayout" label="用户名">
          {{ this.$store.state.username }}
        </a-form-item>
        <a-form-item v-bind="formItemLayout" label="类型">
          <span v-if="this.$store.state.usertype === 'individual'">个人</span>
          <span v-if="this.$store.state.usertype === 'developer'">开发者</span>
          <span v-if="this.$store.state.usertype === 'admin'">管理员</span>
        </a-form-item>
        <a-form-item v-bind="formItemLayout" label="邮箱">
          {{ email }}
        </a-form-item>
        <a-form-item v-bind="formItemLayout" label="电话">
          {{ tel }}
        </a-form-item>
        <a-form-item v-bind="tailFormItemLayout">
          <a-button type="primary" @click="showModal">
            修改密码
          </a-button>
          <a-modal
            title="修改密码"
            :visible="visible"
            :confirm-loading="confirmLoading"
            @ok="handleOk"
            @cancel="handleCancel"
          >
            <a-form-item v-bind="formItemLayout" label="密码" has-feedback>
              <a-input-password
                  v-decorator="[
                  'password',
                  {
                      rules: [
                      {
                          validator: validateToNextPassword,
                      }
                      ],
                  },
                  ]"
                  type="password"
              />
            </a-form-item>
            <a-form-item v-bind="formItemLayout" label="二次确认密码" has-feedback>
              <a-input-password
                v-decorator="[
                'confirm',
                {
                  rules: [
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
          </a-modal>
        </a-form-item>
        <a-form-item v-bind="tailFormItemLayout">
          <a-button type="primary" @click="showModal2">
            修改个人信息
          </a-button>
          <a-modal
            title="修改个人信息"
            :visible="visible2"
            :confirm-loading="confirmLoading2"
            @ok="handleOk2"
            @cancel="handleCancel2"
          >
            <a-form id="change-form" :form="form" @submit="handleSubmit" style="width: 74%; margin: 40px">
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
            </a-form>
          </a-modal>
        </a-form-item>
      </a-form>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script>
function getBase64 (img, callback) {
  const reader = new FileReader()
  reader.addEventListener('load', () => callback(reader.result))
  reader.readAsDataURL(img)
}
export default {
  name: 'User',
  data () {
    return {
      email: '',
      tel: '',
      visible: false,
      confirmLoading: false,
      visible2: false,
      confirmLoading2: false,
      visible3: false,
      confirmLoading3: false,
      loading: false,
      imageUrl: '',
      avatarSrc: '..\\.' + this.$store.state.avatarSrc,
      headers: {
        authorization: 'authorization-text'
      },
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
    this.form = this.$form.createForm(this, { name: 'user' })
  },
  methods: {
    queryUserInfo (e) {
      if (this.$store.state.usertype === 'individual') {
        this.$axios.post('http://127.0.0.1:5000/getUserTable', {
          'userID': this.$route.params.id
        }).then((response) => {
          console.log(response.data)
          this.email = response.data.email
          this.tel = response.data.userTel
        }).catch((e) => {
        })
      } else if (this.$store.state.usertype === 'developer') {
        this.$axios.post('http://127.0.0.1:5000/queryDeveloper', {
          'developerID': this.$route.params.id
        }).then((response) => {
          console.log(response.data)
          this.email = response.data.developerEmail
          this.tel = response.data.developerTel
        }).catch((e) => {
        })
      }
    },
    changeToLogin () {
      this.$router.push('/Login')
      this.$store.commit('changeUser', {})
      this.$store.state.logged = false
    },
    handleChange (info) {
      if (info.file.status === 'uploading') {
        this.loading = true
        return
      }
      if (info.file.status === 'done') {
        if (this.$store.state.usertype === 'individual') {
          this.$axios.post('http://127.0.0.1:5000/changeUserInfor',
            {
              'userID': this.$store.state.userID,
              'userGraph': info.file.response.userGraphPath
            }).then((response) => {
            this.$notification.success({
              message: '修改头像成功',
              description: '重新登录后生效'
            })
          }).catch((e) => {
            this.$notification.error({
              message: '修改头像失败'
            })
          })
          console.log(info.file.response.userGraphPath)
          setTimeout(this.changeToLogin, '2000')
        } else if (this.$store.state.usertype === 'developer') {
          this.$axios.post('http://127.0.0.1:5000/changeDeveloperInfor',
            {
              'developerID': this.$store.state.userID,
              'developerGraph': info.file.response.userGraphPath
            }).then((response) => {
            this.$notification.success({
              message: '修改头像成功'
            })
          }).catch((e) => {
            this.$notification.error({
              message: '修改头像失败'
            })
          })
          console.log(info.file.response.userGraphPath)
          setTimeout(this.changeToLogin, '2000')
        }
        getBase64(info.file.originFileObj, imageUrl => {
          this.imageUrl = imageUrl
          this.loading = false
        })
      }
    },
    beforeUpload (file) {
      const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
      if (!isJpgOrPng) {
        this.$message.error('You can only upload JPG file!')
      }
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('Image must smaller than 2MB!')
      }
      return isJpgOrPng && isLt2M
    },
    onSuccess (file) {
      console.log('1')
    },
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.$axios.post('http://127.0.0.1:5000/changeUserInfor',
            {
              'userID': this.$store.state.userID,
              'userPassword': values.password
            }).then((response) => {
            this.$notification.success({
              message: '修改密码成功'
            })
            this.queryUserInfo()
          }).catch((e) => {
            this.$notification.error({
              message: '修改密码失败'
            })
          })
        }
      })
    },
    handleSubmit2 (e) {
      e.preventDefault()
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.$axios.post('http://127.0.0.1:5000/changeUserInfor',
            {
              'userID': this.$store.state.userID,
              'userTel': values.userTel,
              'email': values.email
            }).then((response) => {
            this.$notification.success({
              message: '修改个人信息成功'
            })
            this.queryUserInfo()
          }).catch((e) => {
            this.$notification.error({
              message: '修改个人信息失败'
            })
          })
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
        callback(new Error('Two passwords that you enter is inconsistent!'))
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
    },
    showModal () {
      this.visible = true
    },
    showModal2 () {
      this.visible2 = true
    },
    showModal3 () {
      this.visible3 = true
    },
    handleOk (e) {
      this.confirmLoading = true
      this.handleSubmit(e)
      this.visible = false
      this.confirmLoading = false
    },
    handleCancel (e) {
      console.log('Clicked cancel button')
      this.visible = false
    },
    handleOk2 (e) {
      this.confirmLoading2 = true
      this.handleSubmit2(e)
      this.visible2 = false
      this.confirmLoading2 = false
    },
    handleCancel2 (e) {
      console.log('Clicked cancel button')
      this.visible2 = false
    },
    handleOk3 (e) {
      this.confirmLoading3 = true
      this.visible3 = false
      this.$store.state.avatarSrc = 'E:\\dbProject\\sdeam-back\\static\\User\\1.jpg'
      this.confirmLoading3 = false
    },
    handleCancel3 (e) {
      console.log('Clicked cancel button')
      this.visible3 = false
    }
  },
  created () {
    if (this.$store.state.logged === true) {
      this.queryUserInfo()
    }
  }
}
</script>

<style scoped>
</style>
