import Vue from 'vue';
import VueGtag from 'vue-gtag';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import router from './router';

Vue.config.productionTip = false;

Vue.use(VueGtag, {
  config: { id: 'UA-154883637-1' },
}, router);

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount('#app');
