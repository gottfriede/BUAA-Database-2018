<template>
  <div class="uploadGame">
    <a-form
    id="uploadGame-form"
    :form="form"
    class="uploadGame-form"
    @submit="handleSubmit"
    style="width: 74%; margin: 40px; margin-top: 100px"
  >
    <a-form-item v-bind="formItemLayout" label="游戏名称">
      <a-input
        v-decorator="[
          'gameName',
          { rules: [{ required: true, message: '请输入游戏名称' }] },
        ]"
        placeholder="名称"
      >
      </a-input>
    </a-form-item>
    <a-form-item v-bind="formItemLayout" label="价格">
        <a-input prefix="￥" suffix="RMB"
        v-decorator="[
          'gamePrice',
          { rules: [{ required: true, message: '请输入游戏价格' }] },
        ]"
        placeholder="价格"
      >
      </a-input>
    </a-form-item>
    <a-form-item v-bind="formItemLayout" label="类型">
        <a-cascader
          v-decorator="[
            'gameType',
            {
              rules: [
                { type: 'array', required: true, message: '请选择用户类型' },
              ],
            },
          ]"
          :options="gametypes"
        />
      </a-form-item>
    <a-form-item v-bind="formItemLayout" label="简介">
      <a-textarea :rows="4"
        v-decorator="[
          'introduction',
          { rules: [{ required: true, message: '请输入游戏简介' }] },
        ]"
        placeholder="简介"
      >
      </a-textarea>
    </a-form-item>
    <a-form-item v-bind="formItemLayout">
      <span slot="label">
        缩略图&nbsp;
        <a-tooltip title="缩略图将用于商店首页展示">
          <a-icon type="question-circle-o" />
        </a-tooltip>
      </span>
      <a-upload
        name="gameGraph"
        list-type="picture-card"
        class="avatar-uploader"
        :show-upload-list="false"
        action="http://127.0.0.1:5000/uploadGameGraph"
        :on-success="onSuccess"
        :before-upload="beforeUpload"
        @change="handleChange"
      >
        <img v-if="imageUrl" :src="imageUrl" width="110" height="110" alt="img" />
        <div v-else>
          <a-icon :type="loading ? 'loading' : 'plus'" />
          <div class="ant-upload-text">
            上传缩略图
          </div>
        </div>
      </a-upload>
    </a-form-item>
    <a-form-item v-bind="formItemLayout">
      <span slot="label">
        详情图&nbsp;
        <a-tooltip title="详情图将用于游戏详情页面展示">
          <a-icon type="question-circle-o" />
        </a-tooltip>
      </span>
      <a-upload
        name="gameDetailGraph"
        list-type="picture-card"
        class="avatar-uploader"
        :show-upload-list="false"
        action="http://127.0.0.1:5000/uploadGameDetailGraph"
        :on-success="onSuccess"
        :before-upload="beforeUpload"
        @change="handleChange2"
      >
        <img v-if="image2Url" :src="image2Url" width="110" height="110" alt="img" />
        <div v-else>
          <a-icon :type="loading2 ? 'loading' : 'plus'" />
          <div class="ant-upload-text">
            上传详情图
          </div>
        </div>
      </a-upload>
    </a-form-item>
    <a-form-item v-bind="tailFormItemLayout" style="margin-left: 33%">
      <a-button type="primary" html-type="submit" style="width: 40%;">
        提交发布
      </a-button>
    </a-form-item>
  </a-form>
  </div>
</template>

<script>
const gametypes = [
  {
    value: 'action',
    label: '动作'
  },
  {
    value: 'adventure',
    label: '冒险'
  },
  {
    value: 'cosplay',
    label: '角色扮演'
  },
  {
    value: 'simulation',
    label: '模拟'
  },
  {
    value: 'relaxation',
    label: '休闲'
  },
  {
    value: 'else',
    label: '其他'
  }
]

function getBase64 (img, callback) {
  const reader = new FileReader()
  reader.addEventListener('load', () => callback(reader.result))
  reader.readAsDataURL(img)
}

export default {
  name: 'UploadGame',
  data () {
    return {
      gametypes,
      loading: false,
      loading2: false,
      imageUrl: '',
      image2Url: '',
      imagePath: '',
      image2Path: '',
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
    this.form = this.$form.createForm(this, { name: 'uploadGame' })
  },
  methods: {
    handleChange (info) {
      if (info.file.status === 'uploading') {
        this.loading = true
        return
      }
      if (info.file.status === 'done') {
        console.log(info.file.response.gameGraphPath)
        this.imagePath = info.file.response.gameGraphPath
        getBase64(info.file.originFileObj, imageUrl => {
          this.imageUrl = imageUrl
          this.loading = false
        })
      }
    },
    handleChange2 (info) {
      if (info.file.status === 'uploading') {
        this.loading2 = true
        return
      }
      if (info.file.status === 'done') {
        console.log(info.file.response.gameDetailGraph)
        this.image2Path = info.file.response.gameDetailGraph
        getBase64(info.file.originFileObj, imageUrl => {
          this.image2Url = imageUrl
          this.loading2 = false
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
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.$axios.post('http://127.0.0.1:5000/uploadGame', {
            'developerID': this.$store.state.userID,
            'gameName': values.gameName,
            'gamePrice': values.gamePrice,
            'introduction': values.introduction,
            'gameType': values.gameType[0],
            'gameGraph': this.imagePath,
            'gameDetailGraph': this.image2Path
          }).then((response) => {
            console.log(response.data)
            this.$notification['success']({
              message: '提交成功'
            })
            this.$router.push('/Library')
          }).catch((e) => {
            this.$notification['error']({
              message: '提交失败',
              description: '游戏名称重复'
            })
          })
        }
      })
    }
  }
}
</script>

<style scoped>
</style>
