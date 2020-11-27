import Vue from 'vue';

import store from './store';
import EditTemplate from './sites/edit_template.vue';
import './styles/main.scss';

new Vue({
  el: '#edit',
  store,
  render: h => h(EditTemplate)
});
