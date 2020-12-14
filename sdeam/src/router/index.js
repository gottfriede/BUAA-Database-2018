import Vue from 'vue'
import Router from 'vue-router'
import Store from '../components/Store'
import About from '../components/About'
import Login from '../components/Login'
import Register from '../components/Register'
import Setting from '../components/Setting'
import User from '../components/User'
import UploadGame from '../components/UploadGame'
import Library from '../components/Library'
import WishList from '../components/WishList'
import GameDetail from '../components/GameDetail'
import WishListDetail from '../components/WishListDetail'
import AdminLogin from '../components/AdminLogin'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/About',
      component: About
    },
    {
      path: '/Login',
      component: Login
    },
    {
      path: '/AdminLogin',
      component: AdminLogin
    },
    {
      path: '/Register',
      component: Register
    },
    {
      path: '/Store',
      component: Store
    },
    {
      path: '/Setting',
      component: Setting
    },
    {
      path: '/User/:type/:id',
      component: User
    },
    {
      path: '/UploadGame',
      component: UploadGame
    },
    {
      path: '/Library',
      component: Library
    },
    {
      path: '/WishList',
      component: WishList
    },
    {
      path: '/WishListDetail/:userID/:wishListID',
      component: WishListDetail
    },
    {
      path: '/GameDetail/:gameID',
      component: GameDetail
    }
  ]
})
