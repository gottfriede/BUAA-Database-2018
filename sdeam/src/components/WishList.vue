<template>
  <div class="library">
    <div v-show="this.$store.state.logged == false">
      <router-link to="/Login">
        <span>登录</span>
      </router-link>
      <span>或</span>
      <router-link to="/Register">
        <span>立即注册</span>
      </router-link>
    </div>
    <div v-show="this.$store.state.logged === true">
      <div v-show="this.$store.state.usertype === 'individual'" style="margin-top: 100px; margin-left: 40px; margin-right: 100px; display: flex; flex-direction: row; flex-wrap: wrap; position: center; width:100%">
        <div v-for="(item,index) in dataSource" :key="index" style="padding: 10px;">
          <div style="text-align:right">
            <font style="font-size: 10px; cursor: pointer;" @click="handleDelete(item.wishListName)">x</font>
          </div>
          <div>
            <img :src="item.imageSrc" style="width: 200px" @click="changeToWishList(item.wishListID)">
          </div>
          <div style="text-align:center">
            <font style="font-size: 20px">{{ item.wishListName }}</font>
          </div>
        </div>
        <div style="padding: 10px; margin-top: 22px">
          <img src="../assets/add.png" style="width: 200px; cursor: pointer;" @click="showModal">
          <a-modal
            title="创建新收藏"
            :visible="visible"
            :confirm-loading="confirmLoading"
            @ok="handleOk"
            @cancel="handleCancel"
          >
            <template slot="footer">
              <a-button type="primary" @click="handleSubmit">
                提交
              </a-button>
            </template>
            <a-form
              id="wishList-form"
              :form="form"
              class="wishList-form"
              style="margin-left: 20px; margin-right: 20px; margin-top: 20px;"
            >
            <a-form-item>
              <a-input
                v-decorator="[
                  'wishListName',
                  { rules: [{ required: true, message: '请输入收藏夹名' }] },
                ]"
                placeholder="收藏夹名"
                v-model="wishListName"
              >
                <a-icon slot="prefix" type="book" style="color: rgba(0,0,0,.25)" />
              </a-input>
            </a-form-item>
            </a-form>
          </a-modal>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
var dataSource = []

export default {
  name: 'WishList',
  data () {
    return {
      dataSource,
      visible: false,
      wishListName: ''
    }
  },
  methods: {
    queryWishList () {
      this.dataSource = []
      let that = this
      this.$axios.post('http://127.0.0.1:5000/queryUserFavorite', {
        'userID': this.$store.state.userID
      }).then((response) => {
        console.log(response.data)
        for (let i = 0; i < response.data.length; i++) {
          let dataItem = {
            imageSrc: '../static/WishList/wishList1.png',
            wishListName: response.data[i].favoriteName,
            wishListID: response.data[i].favoriteID
          }
          this.dataSource.push(dataItem)
        }
      }).catch((e) => {
        that.dataSource = []
      })
      console.log(dataSource)
    },
    handleDelete (wishListName) {
      this.$axios.post('http://127.0.0.1:5000/deleteFavorite', {
        'userID': this.$store.state.userID,
        'favoriteName': wishListName
      }).then((response) => {
        this.queryWishList()
      }).catch((e) => {
      })
    },
    showModal () {
      this.visible = true
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
    changeToWishList (wishListID) {
      this.$router.push('/WishListDetail/' + this.$store.state.userID + '/' + wishListID)
    },
    handleSubmit () {
      this.$axios.post('http://127.0.0.1:5000/createFavorite', {
        'userID': this.$store.state.userID,
        'favoriteName': this.wishListName
      }).then((response) => {
        this.$notification.success({
          message: '创建新收藏成功'
        })
        this.wishListName = ''
        this.visible = false
        this.queryWishList()
      }).catch((e) => {
        this.$notification.error({
          message: '创建新收藏失败'
        })
      })
    }
  },
  created () {
    this.queryWishList()
  }
}
</script>

<style scoped>
</style>
