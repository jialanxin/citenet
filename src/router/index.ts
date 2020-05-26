import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import DataTable from '../views/DataTable.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: DataTable,
  },
  {
    path: '/doi/:doi',
    name: 'Details',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Details.vue'),
  },
  { path: '/Graph', name: 'Graph', component: () => import('../views/Graph.vue') },
];

const router = new VueRouter({
  routes,
});

export default router;
