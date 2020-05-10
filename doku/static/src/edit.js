import Vue from 'vue';
import feather from 'feather-icons';

import store from './store'
import Edit from './sites/edit.vue';
import './styles/main.scss';

new Vue({
  el: '#edit',
  store,
  render: h => h(Edit),
  mounted: () => feather.replace()
});
