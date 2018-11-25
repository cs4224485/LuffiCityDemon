<template>
    <div>
      <h1>课程详细页面</h1>
      <div>
        <p>{{detail.course}}</p>
        <p>{{detail.img}}</p>
        <p>{{detail.level}}</p>
        <p>{{detail.slogan}}</p>
        <p>{{detail.title}}</p>
        <p>{{detail.why}}</p>
        <div>
          <ul v-for="item in detail.chapter">
            <li>{{item.name}}</li>
          </ul>
        </div>
        <div>
          <h3>推荐课程</h3>
          <ul v-for="item in detail.recommends">
            <!--<li><router-link :to="{name:'detail', params:{id:item.id}}">{{item.title}}</router-link></li>-->
            <li @click="changeDetail(item.id)">{{item.title}}</li>
          </ul>
        </div>
      </div>
    </div>
</template>

<script>
    export default {
        name: "detail",
        data(){
          return {
            detail:{
              chapter:[],
              recommends:[],
              course:null,
              img:null,
              slogan:null,
              title:null,


            }
          }
        },
        mounted(){
          var nid = this.$route.params.id;
          this.initDetail(nid)
        },
        methods:{
          initDetail(nid){

            var that = this;
            this.$axios.request({
              url:this.$store.state.apiList.courseDetail,
              method:'GET'
            }).then(function (data) {
              console.log(arg);
              if(arg.data.code === 1000){
                  that.detail =arg.data.data
              }else {
                alert(arg.data.error)
              }
            })
          },
          changeDetail(id){
            // 切换课程详细页面
            this.initDetail();
            // 路由重定向
            this.$router.push({name:'detail', params:{id:id}})
          }
        }
    }
</script>

<style scoped>

</style>
