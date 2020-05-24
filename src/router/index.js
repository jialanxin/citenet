import Vue from 'vue'
import VueRouter from 'vue-router'
import DataTable from '../views/DataTable.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Articles',
    component: DataTable
  },
  {
    path: '/doi/:doi',
    name: 'Details',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Details.vue')
  },
  {
    path: '/graph',
    name: 'Graph',
    component: () => import('../views/Graph.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router