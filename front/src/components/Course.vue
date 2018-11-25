<template>
  <div>
    <h1>课程列表</h1>
    <ul v-for="row in courseList">
      <li><router-link :to="{name:'detail', params:{id:row.id}}">{{row.title}}</router-link></li>
    </ul>
    <div v-for="row in courseList">
      <div style="width: 350px; float: left">
        <img :src="row.course_img"/>
        <h3>{{row.title}}</h3>
        <p>{{row.level}}</p>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: "course",
        data(){
          return{courseList:[]}
        },
        methods:{
          initCourse(){
            // 通过ajax向接口发送请求获取课程列表
            // axios发送ajax
            // 安装axios npm instal axios --save
            // 第一步在main.js中配置
            // 第二步使用axios发送请求
            var that = this;
            this.$axios.request({
              url:this.$store.apiList.course,
              method:'GET'
            }).then(function (ret) {
               // 回调函数 ajax请求发送成功后获取响应内容
               if(ret.data.code === 1000){
                 that.courseList = ret.data.data;
                 console.log(that.courseList)
               }
            }).catch(function () {
               // 如果发生了异常执行此处代码
            })
          }
        },
        mounted(){
          this.initCourse()
        }
    }
</script>

<style scoped>

</style>
