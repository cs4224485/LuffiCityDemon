import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Course from '@/components/Course'
import index from '@/components/index'
import micro from '@/components/micro'
import news from '@/components/news'
import Detail from '@/components/Detail'
import Login from '@/components/login'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/index',
      name: 'index',
      component: index,

    },
    {
      path: '/course',
      name: 'Course',
      component: Course
    },
    {
      path:'/detail/:id',
      name:'detail',
      component:Detail
    },
    {
      path: '/micro',
      name: 'micro',
      component: micro,
      meta:{
        requiredAuth:true
      }
    },
    {
      path: '/news',
      name: 'news',
      component: news
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },

  ],
    mode:'history'
})
