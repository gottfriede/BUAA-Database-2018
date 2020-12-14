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
      <div v-show="this.$store.state.usertype === 'developer'">
        <a-table :columns="columns2" :data-source="datasource2" bordered rowKey="gameName"
          style="margin-left: 200px; margin-right: 200px; margin-top: 50px">
          <template slot="operation" slot-scope="text, record">
            <a-popconfirm
              title="确定要删除吗?"
              @confirm="() => handleDelete(record.gameName)"
            >
              <a href="javascript:;">下架</a>
            </a-popconfirm>
          </template>
          <img  style="width:150px;heigth:50px" slot="pic" slot-scope="text, record" :src=record.gameGraph />
          <template slot="title">
            您发布的游戏
            <span style="margin-left: 70%">
              <router-link to="/UploadGame">
                在SDEAM上发布您的新游戏！
              </router-link>
            </span>
          </template>
        </a-table>
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
  </div>
</template>

<script>
const columns2 = [
  {
    title: '图片',
    dataIndex: 'gameGraph',
    key: 'gameGraph',
    scopedSlots: {
      customRender: 'pic'
    }
  },
  {
    title: '名称',
    dataIndex: 'gameName',
    key: 'gameName'
  },
  {
    title: '价格(￥)',
    dataIndex: 'gamePrice',
    key: 'gamePrice'
  },
  {
    title: '操作',
    dataIndex: 'operation',
    key: 'operation',
    scopedSlots: {
      customRender: 'operation'
    }
  }
]

var dataSource = []
var datasource2 = []

export default {
  name: 'Library',
  data () {
    return {
      dataSource,
      columns2,
      datasource2
    }
  },
  methods: {
    queryGameTable () {
      this.dataSource = []
      let that = this
      if (this.$store.state.usertype === 'individual') {
        this.$axios.post('http://127.0.0.1:5000/queryUserGames', {
          'userID': this.$store.state.userID
        }).then((response) => {
          console.log(response.data)
          for (let i = 0; i < response.data.length; i++) {
            let dataItem = {
              imageSrc: response.data[i].gameDetailGraph,
              gameName: response.data[i].gameName,
              gameID: response.data[i].gameID
            }
            this.dataSource.push(dataItem)
          }
        }).catch((e) => {
        })
      } else if (this.$store.state.usertype === 'developer') {
        this.$axios.post('http://127.0.0.1:5000/queryDeveloperGames', {
          'developerID': this.$store.state.userID
        }).then((response) => {
          that.datasource2 = response.data
        }).catch((e) => {
          that.datasource2 = []
        })
        console.log(datasource2)
      }
    },
    handleDelete (gameName) {
      this.$axios.post('http://127.0.0.1:5000/deleteGame', {
        'developerID': this.$store.state.userID,
        'gameName': gameName
      }).then((response) => {
        this.$notification['success']({
          message: '下架成功'
        })
        this.queryGameTable(1)
      }).catch((e) => {
        this.$notification['error']({
          message: '下架失败'
        })
      })
    },
    changeToGameDetail (gameID) {
      this.$router.push('/GameDetail/' + gameID)
    }
  },
  created () {
    this.queryGameTable()
  }
}
</script>

<style scoped>
</style>
