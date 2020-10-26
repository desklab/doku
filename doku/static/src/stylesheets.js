import Vue from 'vue';

import store from './store'
import Stylesheets from './sites/stylesheets.vue';
import './styles/main.scss';

new Vue({
  el: '#stylesheets',
  store,
  render: h => h(Stylesheets)
});
