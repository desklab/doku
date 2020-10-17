import Vue from 'vue';

import store from './store'
import Resources from './sites/templates.vue';
import './styles/main.scss';

new Vue({
  el: '#templates',
  store,
  render: h => h(Templates)
});
