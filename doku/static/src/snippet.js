import Vue from 'vue';

import store from './store';
import Snippet from './sites/snippet.vue';
import './styles/main.scss';

new Vue({
  el: '#snippet',
  store,
  render: h => h(Snippet)
});
