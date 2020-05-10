import Vue from 'vue';
import Home from './sites/main.vue';
import './styles/main.scss';
import feather from 'feather-icons';

new Vue({
  el: '#app',
  render: h => h(Home),
  mounted: () => feather.replace()
});
