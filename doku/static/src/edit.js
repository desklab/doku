import Vue from 'vue';
import Edit from './sites/edit.vue';
import feather from 'feather-icons';
import './styles/main.scss';

new Vue({
  el: '#edit',
  render: h => h(Edit),
  mounted: () => feather.replace()
});
