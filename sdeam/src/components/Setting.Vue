<template>
  <div class="setting">
    <p>Setting Page</p>
    <button @click="test()">test</button>
  </div>
</template>

<script>
export default {
  name: 'Setting',
  data () {
    return {
    }
  },
  methods: {
    test () {
      console.log(this.$store.state)
    }
  }
}
</script>

<style scoped>
</style>
