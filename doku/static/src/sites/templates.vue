<template>
  <div>
    <template-item ref="template_item" v-for="template in templates" :key="template.id" :template="template"></template-item>
  </div>
</template>

<script>
    import templateApi from '../api/template';
    import TemplateItem from '../components/ui/TemplateItem';

    import {mapState, mapActions} from 'vuex';
    import * as actionTypes from '../store/types/actions';


    export default {
      name: 'Templates',
      components: {
        TemplateItem
      },
      computed: mapState({
        templates: state => state.template.templates
      }),
      methods: {
        ...mapActions('template', [
          actionTypes.CREATE_TEMPLATE,
        ])
      }
    }
</script>

<style scoped>
</style>
