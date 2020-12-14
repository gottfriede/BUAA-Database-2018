<template>
  <div class="about">
    <a-card size="small" title="Contact us" style="width: 300px, align: center">
      <p>Gottfried</p>
      <p>cjbbbbbbbb</p>
      <p>A cat</p>
    </a-card>
    <a-button @click="go"></a-button>
  </div>
</template>

<script>
export default {
  name: 'About',
  data () {
    return {
    }
  },
  methods: {
    hello () {
      this.$axios.get('http://127.0.0.1:5000/hello').then((response) => {
        console.log(response)
      }).catch((e) => {
        console.log('error')
      })
    },
    change () {
      this.$router.push('/uploadGame')
    },
    go () {
      let data = {
        userID: 1,
        favoriteName: 's'
      }
      this.$axios.post('http://127.0.0.1:5000/querySingleFavorite', data).then((res) => {
        console.log(res)
      })
    }
  }
}
</script>

<style scoped>
</style>
