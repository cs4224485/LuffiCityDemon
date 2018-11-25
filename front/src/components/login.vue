<template>
  <div>
    <h1>用户登录</h1>

    <p>
      <input type="text" v-model="username"/>
    </p>
    <p>
      <input type="password" v-model="password"/>
    </p>
    <input type="button" value="登录" @click="doLogin"/>
  </div>
</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        username:'',
        password:''
      }
    },
    methods:{
      doLogin(){
        var that = this;
        this.$axios.request({
          url:this.store.apiList.auth,
          data:{
            user:this.username,
            pwd:this.password
          },
          method:'POST',
          headers:{
            'Content-Type':'application/json'
          }
        }).then(function (arg) {
          if (arg.data.code === 1000){
            console.log(arg)
            that.$store.state.token = arg.data.token;
            that.$store.state.username = that.username;
            that.$store.commit('saveToken', {token:arg.data.token, username:that.username})
            var url = that.$route.query.backUrl;
            console.log(url);
            if(url){
              that.$router.push({path:url})
            }else {
              that.$router.push({path:'/index'})
            }
          }else {
            alert(arg.data.error)
          }
        }).catch(function (arg) {
          console.log('发送错误')
        })
      }
    }
  }
</script>

<style scoped>

</style>
