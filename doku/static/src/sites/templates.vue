<template>
  <div>
    <div class="doku-document-toolbar">
      <h3 class="m-0">Templates</h3>
      <button @click="openModal" class="btn btn-sm">
        <plus-icon size="18"></plus-icon>
        Create new template
      </button>
    </div>

    <template-item ref="template_item" v-for="template in templates" :key="template.id" :template="template"></template-item>
  
    <modal ref="modal" v-bind:title="'New Template'">
      <div class="modal-body">
        <div class="content">
          <div class="form-group p-2">
            <label class="form-label" for="templateNameInput">Name</label>
            <input v-on:keyup="$event.target.classList.remove('is-error')" name="name" class="form-input" type="text" id="templateNameInput" placeholder="Name" pattern="^.{1,}$" required>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button @click="saveNewTemplate" class="btn btn btn-primary">
          Save
        </button>
        <button @click="closeModal" class="btn btn-link">
          Close
        </button>
      </div>
    </modal>
  
  </div>
</template>

<script>
    import templateApi from '../api/template';
    import TemplateItem from '../components/template/TemplateItem';

    import {PlusIcon} from 'vue-feather-icons';
    import Modal from '../components/ui/modal/Modal.vue';
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
        openModal() {
          this.$refs.modal.open();
        },
        closeModal() {
          this.$refs.modal.close();
        },
        saveNewTemplate(event) {
          let TemplateNameInput = document.getElementById('templateNameInput');

          if (!templateNameInput.checkValidity()) {
            templateNameInput.classList.add('is-error');
            return;
          }
          event.target.classList.add('loading');

          let data = {
            name: templateNameInput.value
          }
          templateApi.createTemplate(data)
            .then((response) => {
              window.location.href = response.data.id;
            })
            .catch(console.error)
            .finally(() => {
              event.target.classList.remove('loading');
            });
        }
      }
    }
</script>

<style scoped>
</style>
