<template>
  <div class="wishListDetail">
    <div v-show="this.$store.state.logged == false">
      <router-link to="/Login">
        <span>登录</span>
      </router-link>
      <span>或</span>
      <router-link to="/Register">
        <span>立即注册</span>
      </router-link>
    </div>
    <div v-show="this.$store.state.usertype === 'individual'" style="margin-top: 100px; margin-left: 40px; margin-right: 100px; display: flex; flex-direction: row; flex-wrap: wrap; position: center; width:100%">
      <div v-for="(item,index) in dataSource" :key="index" style="padding: 10px;">
        <div>
          <img :src="item.imageSrc" style="width: 300px" @click="changeToGameDetail(item.gameID)">
        </div>
        <div style="text-align:center">
          <font style="font-size: 20px">{{ item.gameName }}</font>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
var dataSource = []

export default {
  name: 'WishListDetail',
  data () {
    return {
      dataSource
    }
  },
  methods: {
    queryWishListDetail () {
      this.dataSource = []
      if (this.$store.state.usertype === 'individual') {
        this.$axios.post('http://127.0.0.1:5000/querySingleFavorite', {
          'userID': this.$store.state.userID,
          'favoriteID': this.$route.params.wishListID
        }).then((response) => {
          console.log(response.data)
          for (let i = 0; i < response.data.length; i++) {
            let dataItem = {
              imageSrc: '..\\.' + response.data[i].gameDetailGraph,
              gameName: response.data[i].gameName,
              gameID: response.data[i].gameID
            }
            this.dataSource.push(dataItem)
          }
        }).catch((e) => {
        })
      }
    }
  },
  created () {
    this.queryWishListDetail()
  }
}
</script>

<style scoped>
</style>
