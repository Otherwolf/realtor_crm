import Vue from 'vue'
import Router from 'vue-router'

import Profile from '@/components/Profile'
import Index from '@/components/Index'
import Lots from '@/components/Lots'
import Complexes from '@/components/Complexes'
import SubComplexes from '@/components/SubComplexes'
import SubDevelopers from '@/components/SubDevelopers'

Vue.use(Router)

export default new Router({
  routes: [{
    name: 'profile',
    path: '/profile',
    component: Profile
  }, {
    path: '/index',
    name: 'index',
    component: Index,
    children: [{
      path: 'lots',
      components: {main: Lots, sub: SubComplexes},
      name: 'lots'
    }, {
      path: 'complexes',
      components: {main: Complexes, sub: SubDevelopers},
      name: 'complexes'
    }]
  },
    {path: '/', redirect: '/index/lots'}
  ]
})
