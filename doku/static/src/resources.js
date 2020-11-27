import Vue from 'vue';

import store from './store';
import Resources from './sites/resources.vue';
import './styles/main.scss';

new Vue({
  el: '#resources',
  store,
  render: h => h(Resources)
});
