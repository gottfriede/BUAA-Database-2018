<template>
  <div class="store">
    <a-row>
      <a-col :span="3"></a-col>
      <a-col :span="18">
        <div style="margin-top: 20px; margin-bottom: 20px;">
          <a-carousel arrows :autoplay="true">
          <div
            slot="prevArrow"
            slot-scope="props"
            class="custom-slick-arrow"
            style="left: 10px;zIndex: 1"
          >
            <a-icon type="left-circle" />
          </div>
          <div slot="nextArrow" slot-scope="props" class="custom-slick-arrow" style="right: 10px">
            <a-icon type="right-circle" />
          </div>
          <div><img src="../assets/cyberpunk.png"></div>
          <div><img src="../assets/laisha.png"></div>
          <div><img src="../assets/tga.png"></div>
          <div><img src="../assets/yuanshen.png"></div>
        </a-carousel>
        </div>
          <a-table :columns="columns" :data-source="datasource" bordered rowKey="gamename">
            <template slot="operation" slot-scope="text, record">
              <a @click="() => changeToDetails(record.gameID)">查看详情</a>
              <a-divider type="vertical" />
              <a @click="() => adminHandleDelete(record.gameID)">{{ deleteFont }}</a>
            </template>
            <img  style="width:200px;heigth:50px" slot="pic" slot-scope="text, record" :src=record.gameGraph />
          </a-table>
        </a-col>
      <a-col :span="3"></a-col>
    </a-row>
  </div>
</template>

<script>
const columns = [
  {
    title: '图片',
    dataIndex: 'gameGraph',
    key: 'gameGraph',
    scopedSlots: {
      customRender: 'pic'
    },
    width: 230
  },
  {
    title: '游戏名称',
    dataIndex: 'gameName',
    key: 'gameName',
    className: 'Gamename'
  },
  {
    title: '价格(￥)',
    dataIndex: 'gamePrice',
    key: 'gamePrice'
  },
  {
    title: '类型',
    dataIndex: 'gameType',
    key: 'gameType'
  },
  {
    title: '操作',
    dataIndex: 'operation',
    key: 'operation',
    scopedSlots: {
      customRender: 'operation'
    },
    width: 200
  }
]

var datasource = []

export default {
  name: 'Store',
  data () {
    return {
      columns,
      datasource,
      deleteFont: ''
    }
  },
  methods: {
    queryGameTable () {
      let that = this
      this.$axios.post('http://127.0.0.1:5000/queryAllGame').then((response) => {
        console.log(response.data)
        that.datasource = response.data
      }).catch((e) => {
        datasource = []
      })
      console.log(datasource)
    },
    adminHandleDelete (gameID) {
      this.$axios.post('http://127.0.0.1:5000/adminDeleteGame', {
        'adminID': this.$store.state.userID,
        'gameID': gameID
      }).then((response) => {
        this.queryGameTable()
        console.log(response.data)
        this.$notification.success({
          message: '删除游戏成功'
        })
      }).catch((e) => {
        this.$notification.error({
          message: '删除游戏失败'
        })
      })
    },
    changeToDetails (gameID) {
      this.$router.push('/GameDetail/' + gameID)
    }
  },
  created () {
    this.queryGameTable()
    if (this.$store.state.usertype === 'admin') {
      this.deleteFont = '删除'
    } else {
      this.deleteFont = ''
    }
  }
}
</script>

<style scoped>
.ant-carousel >>> .slick-slide {
  text-align: center;
  height: 260px;
  line-height: 160px;
  background: #364d79;
  overflow: hidden;
}

.ant-carousel >>> .custom-slick-arrow {
  width: 25px;
  height: 25px;
  font-size: px;
  color: #fff;
  background-color: rgba(31, 45, 61, 0.11);
  opacity: 0.3;
}
.ant-carousel >>> .custom-slick-arrow:before {
  display: none;
}
.ant-carousel >>> .custom-slick-arrow:hover {
  opacity: 0.5;
}

.ant-carousel >>> .slick-slide h3 {
  color: #fff;
}

.Gamename {
  font-size: 100px;
}
</style>
