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
  mounted() {}
};
</script>

<style scoped>
</style>
