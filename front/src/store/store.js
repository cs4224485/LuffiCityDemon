import Vue from 'vue'
import Vuex from 'vuex'
import Cookie from 'vue-cookies'

Vue.use(Vuex);

export default new Vuex.Store({
  // 组件中通过 this.$store.state.username调用
  state:{
    username: Cookie.get("username"),
    token: Cookie.get("token"),
    apiList:{
       course:'http://127.0.0.1:8000/api/v1/course/',
       courseDetail:"http://127.0.0.1:8000/api/v1/course/"+ nid + "/",
       auth:'http://127.0.0.1:8000/api/v1/auth/',
       micro:'http://127.0.0.1:8000/api/v1/micro/'
    }

  },
  mutations:{
    // 组件中通过 this.$store.commit(参数) 调用
    saveToken:function (state, userToken) {
      state.username = userToken.username;
      state.token = userToken.token;
      Cookie.set("username", userToken.username, "20min");
      Cookie.set("token", userToken.token, "20min");
      console.log(Cookie)
    },
    clearToke:function (state) {
        state.username = null;
        state.token = null;
        Cookie.remove('username')
        Cookie.remove('token')
    }
  }
})
