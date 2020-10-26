<template>
  <div>
    <div class="border rounded p-4 my-2 bg-gray">
      <label class="form-switch">
          <input v-model="showBaseStyles" id="showBaseStyles" type="checkbox">
          <i class="form-icon"></i>
          Show Base-Stylesheets
      </label>
      
    </div>
    <div v-if="showBaseStyles">
      <StyleItem v-for="style in stylesheets"  class="mb-2" v-bind:stylesheet="style" :key="style.id"></StyleItem>
    </div>
    <div v-if="!showBaseStyles">
      <StyleItem v-for="style in stylesheets.filter(style=>!style.base_templates[0])"  class="mb-2" v-bind:stylesheet="style" :key="style.id"></StyleItem>
    </div>
  </div>
</template>

<script>
    import stylesheetApi from '../api/stylesheet';
    import StyleItem from '../components/stylesheet/StyleItem';

    import {mapState, mapActions} from 'vuex';
    import * as actionTypes from '../store/types/actions';

    export default {
      name: 'Resources',
      components: {
        StyleItem
      },
      data() {
        return {
          showBaseStyles: true,
        }
      },
      computed: mapState({
        stylesheets: state => state.stylesheet.stylesheets,
      }),
      mounted() {
        stylesheetApi.fetchStylesheets().then(res => this.allStylesheets = res.data.result);
      },
      methods: {
        ...mapActions('template', [
          actionTypes.ADD_STYLESHEET_TO_TEMPLATE,
        ]),
        add() {
          let url = this.add_stylesheet_url;
          stylesheetApi.createStylesheet({name: 'New Stylesheet'})
            .then(res => {
              this.addStylesheet({url: url, data: {id: style.data.id}});
            });
        }
      }
    }
</script>

<style scoped>
</style>
