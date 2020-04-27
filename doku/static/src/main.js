import Vue from 'vue';
import Home from './sites/main.vue';
import './styles/main.scss';

new Vue({
  el: '#app',
  render: h => h(Home),
});
