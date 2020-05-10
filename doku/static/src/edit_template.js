import Vue from 'vue';
import feather from 'feather-icons';

import store from './store'
import EditTemplate from './sites/edit_template.vue';
import './styles/main.scss';

new Vue({
  el: '#edit',
  store,
  render: h => h(EditTemplate),
  mounted: () => feather.replace()
});
