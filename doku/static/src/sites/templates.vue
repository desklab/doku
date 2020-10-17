<template>
  <div>
    <button @click="openModal" class="btn btn-sm">
    <plus-icon size="18"></plus-icon>
    Create new template
  </button>
    <template-item ref="template_item" v-for="template in templates" :key="template.id" :template="template"></template-item>
  </div>
</template>

<script>
    import templateApi from '../api/template';
    import TemplateItem from '../components/ui/TemplateItem';

    import {PlusIcon} from 'vue-feather-icons';
    import Modal from '../components/ui/Modal.vue';
    import {mapState, mapActions} from 'vuex';
    import * as actionTypes from '../store/types/actions';

    export default {
      name: 'Templates',
      components: {
        TemplateItem, Modal, PlusIcon
      },
      data() {
        return {
          templates: []
        }
      },
      mounted() {
        templateApi.fetchTemplates()
          .then((response) =>{
            this.templates = response.data.result;
          })
          .catch(console.error);
      },
      methods: {
        ...mapActions('template', [
          actionTypes.CREATE_TEMPLATE,
        ]),
        openModal() {
        // ToDo
        },
      }
    }
</script>

<style scoped>
</style>
