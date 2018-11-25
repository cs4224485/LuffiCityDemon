<template>
  <div>
    <h1>LuffyX学位:{{title}}</h1>
  </div>
</template>

<script>
    export default {
        name: "micro",
        data(){
          return {
            title:null
          }
        },
        mounted(){
          this.initMicro()
        },
        methods:{
          initMicro(){
            var that = this;
            this.$axios.request({
              url: this.store.apiList.micro,
              method:'GET',
              params:{
                token:this.$store.state.token
              }
            }).then(function (arg) {
              console.log(arg)

              if (arg.data.code === 1000 ){
                  console.log(arg.data.title);
                  that.title = arg.data.title
              }
            })
          }

        }

    }
</script>

<style scoped>

</style>
