<template>
  <div>
    <StyleItem
      v-for="style in stylesheets"
      :key="style.id"
      class="mb-2"
      :stylesheet="style"
    />
  </div>
</template>

<script>
import {mapState} from 'vuex';

import stylesheetApi from '../api/stylesheet';
import StyleItem from '../components/stylesheet/StyleItem';


export default {
  name: 'Resources',
  components: {
    StyleItem
  },
  data() {
    return {
      showBaseStyles: true,
    };
  },
  computed: mapState({
    stylesheets: state => state.stylesheet.stylesheets,
  }),
  mounted() {
    stylesheetApi.fetchStylesheets().then(res => this.allStylesheets = res.data.result);
  }
};
</script>

<style scoped>
</style>
