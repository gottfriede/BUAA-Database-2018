<template>
  <div class="gameDetail">
    <a-row>
      <a-col :span="6">
      </a-col>
      <a-col :span="8">
        <div style="margin-top: 50px; margin-bottom: 20px">
          <font style="font-size:40px">{{ gamename }}</font>
        </div>
        <img :src="detailImgSrc" style="width:90%; margin-bottom: 30px">
        <a-card style="width: 90%">
          立即在SDEAM上购买《
          <span>{{ gamename }}</span>
          》
          <span style="margin-left: 70px; float: right">
            ￥{{ gameprice }}
            <a-button type="primary" @click="handleBuy">
              购买
            </a-button>
            <a-modal
              v-model="modalVisible"
              title="订单"
              centered
              width="1000px"
            >
              <template slot="footer">
                <a-button v-if="current < steps.length - 1" type="primary" @click="next" :disabled="disable">
                  下一步
                </a-button>
                <a-button
                  v-if="current == steps.length - 1"
                  type="primary"
                  @click="buyDone"
                >
                  完成
                </a-button>
              </template>
              <a-steps :current="current">
                <a-step v-for="item in steps" :key="item.title" :title="item.title" />
              </a-steps>
              <div class="steps-content">
                <template v-if="current === 0">
                  <div style="margin-top: 100px; margin-bottom: 100px; margin-left: 250px">
                    <font style="font-size:20px">用户名： {{ this.$store.state.username }}</font>
                    <br>
                    <font style="font-size:20px">游戏名： {{ this.gamename }}</font>
                    <br>
                    <font style="font-size:20px">价格    ： ￥{{ this.gameprice }}</font>
                  </div>
                </template>
                <template v-if="current === 1">
                  <div style="margin-top: 10px">
                    <font style="font-size:15px">订单号： {{ this.buyID }}</font>
                  </div>
                  <div style="text-align: center">
                    <img src="../assets/QRcode.png" style="width:300px; height: 300px; margin-top: 20px">
                    <br>
                    <font style="font-size:30px">￥ {{ this.gameprice }}</font>
                  </div>
                </template>
                <template v-if="current === 2">
                  <div style="margin-top: 100px; margin-bottom: 100px">
                    <div style="text-align: center">
                      <a-icon type="loading" style="font-size: 100px"/>
                    </div>
                    <p style="text-align: center; margin-top: 30px">
                      <font style="font-size: 20px">确认支付结果中...</font>
                    </p>
                  </div>
                </template>
                <template v-if="current === 3">
                  <div style="margin-top: 100px; margin-bottom: 100px; margin-left: 250px">
                    <font style="font-size:20px">订单号： {{ this.buyID }}</font>
                    <br>
                    <font style="font-size:20px">用户名： {{ this.$store.state.username }}</font>
                    <br>
                    <font style="font-size:20px">游戏名： {{ this.gamename }}</font>
                    <br>
                    <font style="font-size:20px">支付额： ￥{{ this.gameprice }}</font>
                    <br>
                    <font style="font-size:20px">下单时间： {{ this.buyTime }}</font>
                    <br>
                    <font style="font-size:20px">订单状态： 已完成</font>
                  </div>
                </template>
              </div>
            </a-modal>
          </span>
        </a-card>
        <a-card style="width: 90%">
          将《
          <span>{{ gamename }}</span>
          》加入您的收藏夹
          <span style="margin-left: 70px; float: right">
            <a-button type="primary" @click="showModal2">
              加入收藏夹
            </a-button>
            <a-modal
              v-model="modalVisible2"
              title="加入收藏夹"
              centered
            >
              <template slot="footer">
                <a-button type="primary" @click="handleAdd">
                  提交
                </a-button>
              </template>
              <a-select default-value="" style="width: 120px">
                <a-select-option v-for="(item,index) in wishNameList" :key="index" :value="item.wishListName" @click="handleClick(item.wishListName)">
                  {{ item.wishListName }}
                </a-select-option>
              </a-select>
            </a-modal>
          </span>
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card title="介绍" style="width: 100%; margin-top: 130px; height: 477px">
          <a-card-grid style="width: 100%">
            <p>{{ gameintroduction }}</p>
          </a-card-grid>
          <a-card-grid style="width: 100%">
            <span>
              <span>开发商   :</span>
              <span style="margin-left: 23px=">{{ developername }}</span>
            </span>
            <br>
            <span>游戏类型 :</span>
            <a-tag color="blue" style="margin-left: 10px">{{ gametype }}</a-tag>
            <br>
            <span>用户评分 :</span>
            <a-rate :default-value="5" :value="rate" disabled />
            <span style="margin-left: 7px">{{ rate }}</span>
          </a-card-grid>
        </a-card>
      </a-col>
      <a-col :span="6">
      </a-col>
    </a-row>
    <a-row style="margin-top: 50px">
      <a-col :span="6">
      </a-col>
      <a-col :span="12">
        <a-card title="撰写您的评价" style="margin-bottom: 50px" v-if="this.$store.state.usertype === 'individual'">
          <div style="margin-bottom: 10px">
            您认为这款游戏有什么优点或缺点？您是否会将这款游戏推荐给他人？请写下您的看法。
          </div>
          <a-avatar :src="avatarSrc" :size="50"/>
          <font style="font-size: 20px; margin-left: 10px">{{ this.$store.state.username }}</font>
          <a-textarea v-model="comment" :rows="5" style="margin-top: 15px; width: 100% "/>
          <div style="margin-bottom: 10px; margin-top: 10px">
            请根据您的总体游戏体验，对本游戏进行评分。
          </div>
          <span>
            <a-rate v-model="commentRate" :tooltips="desc" />
            <span class="ant-rate-text">{{ desc[commentRate - 1] }}</span>
            <a-button type="primary" @click="handleCommit" style="float: right" v-if="!hasComment">提交</a-button>
            <a-button type="primary" @click="handleDelete" style="float: right" v-if="hasComment">删除</a-button>
          </span>
        </a-card>
        <font style="font-size:20px">消费者评价</font>
        <a-list item-layout="horizontal" :data-source="commentList">
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a slot="actions" @click="adminHandleDelete(item.commentID)">
              <font>{{ deleteFont }}</font>
            </a>
            <a-list-item-meta
              :description="item.comment"
            >
              <a slot="title" href="https://www.antdv.com/">{{ item.userName }}</a>
              <a-avatar
                slot="avatar"
                :src="item.userGraph"
              />
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </a-col>
      <a-col :span="6">
      </a-col>
    </a-row>
  </div>
</template>

<script>
var commentList = []
var wishNameList = []

export default {
  name: 'GameDetail',
  data () {
    return {
      gamename: 'cyberpunk 2077',
      gameprice: '298',
      gametype: '角色扮演',
      developername: 'CD PROJEKT RED',
      detailImgSrc: '..\\static\\Game\\3.png',
      gameintroduction: '   《赛博朋克 2077》是一款开放世界游戏，故事发生在夜之城，权力更迭和身体改造是这里不变的主题。扮演一名野心勃勃的雇佣兵：V，追寻一种独一无二的植入体——获得永生的关键。自定义角色义体、技能和玩法，探索包罗万象的城市。您做出的选择也将会对剧情和周遭世界产生影响。',
      rate: '3.9',
      modalVisible: false,
      modalVisible2: false,
      commentList,
      current: 0,
      disable: false,
      buyID: '777777777',
      buyTime: '',
      comment: '',
      commentRate: '3',
      hasComment: false,
      wishNameList,
      wishListToAdd: '',
      deleteFont: '',
      desc: ['体验糟糕', '多半差评', '差强人意', '多半好评', '相当出色'],
      avatarSrc: '.' + this.$store.state.avatarSrc,
      steps: [
        {
          title: '确认订单',
          content: '确认'
        },
        {
          title: '付款',
          content: '付款'
        },
        {
          title: '确认支付结果',
          content: ''
        },
        {
          title: '订单结果',
          content: '结果'
        }
      ]
    }
  },
  methods: {
    changeStatus () {
      this.current++
      this.disable = false
    },
    next () {
      this.current++
      if (this.current === 1) {
        this.$axios.post('http://127.0.0.1:5000/buyGame', {
          'userID': this.$store.state.userID,
          'gameName': this.gamename
        }).then((response) => {
          console.log(response.data)
          this.buyID = response.data.buyID
          this.buytime = response.data.buyTime
        }).catch((e) => {
          this.$notification.error({
            message: '购买失败',
            description: '您的库中已拥有此游戏，请移步库中查看'
          })
          this.disable = true
          this.current--
        })
      }
      if (this.current === 2) {
        this.disable = true
        setTimeout(this.changeStatus, '2000')
        this.$axios.post('http://127.0.0.1:5000/confirmGame', {
          'userID': this.$store.state.userID,
          'buyID': this.buyID
        }).then((response) => {
          console.log(response.data)
        }).catch((e) => {
        })
      }
    },
    buyDone () {
      this.$notification.success({
        message: '购买成功',
        description: '请移步库中查看'
      })
      this.modalVisible = false
      this.current = 0
    },
    queryGameDetail (gameID) {
      console.log(gameID)
      this.$axios.post('http://127.0.0.1:5000/queryGame', {
        'userID': this.$store.state.userID,
        'gameID': gameID
      }).then((response) => {
        console.log(response.data)
        this.gamename = response.data.gameName
        this.gameprice = response.data.gamePrice
        this.gametype = response.data.gameType
        this.developername = response.data.developerName
        this.detailImgSrc = '.' + response.data.gameDetailGraph
        this.gameintroduction = response.data.introduction
        this.rate = response.data.gradeAvg
        this.commentList = response.data.comments
        console.log(this.commentList.length)
        for (let i = 0; i < this.commentList.length; i++) {
          this.commentList[i].userGraph = '.' + this.commentList[i].userGraph
          if (this.commentList[i].userName === this.$store.state.username) {
            this.comment = this.commentList[i].comment
            this.hasComment = true
          }
        }
        if (!this.detailImgSrc) {
          this.detailImgSrc = '../static/Game/3.png'
        }
      }).catch((e) => {
      })
    },
    handleBuy () {
      if (this.$store.state.logged === false) {
        this.$notification.error({
          message: '购买失败',
          description: '您还没有登录'
        })
      } else if (this.$store.state.usertype === 'developer') {
        this.$notification.warning({
          message: '抱歉',
          description: '暂不支持开发者账号购买游戏，请申请个体账号'
        })
      } else if (this.$store.state.usertype === 'individual') {
        this.modalVisible = true
        this.buyTime = new Date()
      }
    },
    handleCommit () {
      this.$axios.post('http://127.0.0.1:5000/addComment', {
        'userID': this.$store.state.userID,
        'gameName': this.gamename,
        'commentContents': this.comment,
        'grade': this.commentRate
      }).then((response) => {
        console.log(response.data)
        this.queryGameDetail(this.$route.params.gameID)
        this.$notification.success({
          message: '添加评论成功'
        })
        this.hasComment = true
      }).catch((e) => {
        this.$notification.error({
          message: '添加评论失败'
        })
      })
    },
    handleDelete () {
      this.$axios.post('http://127.0.0.1:5000/deleteComment', {
        'userID': this.$store.state.userID,
        'gameName': this.gamename
      }).then((response) => {
        this.queryGameDetail(this.$route.params.gameID)
        console.log(response.data)
        this.$notification.success({
          message: '删除评论成功'
        })
        this.hasComment = false
        this.comment = ''
      }).catch((e) => {
        this.$notification.error({
          message: '删除评论失败'
        })
      })
    },
    adminHandleDelete (commentID) {
      this.$axios.post('http://127.0.0.1:5000/adminDeleteComment', {
        'adminID': this.$store.state.userID,
        'commentID': commentID
      }).then((response) => {
        this.queryGameDetail(this.$route.params.gameID)
        console.log(response.data)
        this.$notification.success({
          message: '删除评论成功'
        })
      }).catch((e) => {
        this.$notification.error({
          message: '删除评论失败'
        })
      })
    },
    showModal2 () {
      if (this.$store.state.logged === false) {
        this.$notification.error({
          message: '购买失败',
          description: '您还没有登录'
        })
      } else if (this.$store.state.usertype === 'developer') {
        this.$notification.warning({
          message: '抱歉',
          description: '暂不支持开发者账号购买游戏，请申请个体账号'
        })
      } else if (this.$store.state.usertype === 'individual') {
        this.modalVisible2 = true
        this.wishNameList = []
        this.queryWishListName()
      }
    },
    queryWishListName () {
      this.$axios.post('http://127.0.0.1:5000/queryUserFavorite', {
        'userID': this.$store.state.userID
      }).then((response) => {
        console.log(response.data)
        for (let i = 0; i < response.data.length; i++) {
          let dataItem = {
            wishListName: response.data[i].favoriteName
          }
          this.wishNameList.push(dataItem)
        }
      }).catch((e) => {
        this.wishListName = []
      })
    },
    handleClick (name) {
      this.wishListToAdd = name
    },
    handleAdd () {
      this.$axios.post('http://127.0.0.1:5000/addFavorite', {
        'userID': this.$store.state.userID,
        'favoriteName': this.wishListToAdd,
        'gameName': this.gamename
      }).then((response) => {
        this.$notification.success({
          message: '添加成功'
        })
        this.wishListToAdd = ''
        this.modalVisible2 = false
      }).catch((e) => {
        this.$notification.warning({
          message: '添加失败',
          description: '收藏夹中已存在此游戏'
        })
      })
    }
  },
  created () {
    this.queryGameDetail(this.$route.params.gameID)
    if (this.$store.state.usertype === 'admin') {
      this.deleteFont = '删除'
    } else {
      this.deleteFont = ''
    }
  }
}
</script>

<style scoped>
</style>
