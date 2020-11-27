<template>
  <div>
    <div class="doku-document-toolbar">
      <h3 class="m-0">
        Templates
      </h3>
      <button class="btn btn-sm" @click="openModal">
        <plus-icon size="18" />
        Create new template
      </button>
    </div>

    <template-item
      v-for="template in templates"
      ref="template_item"
      :key="template.id"
      :template="template"
    />

    <modal ref="modal" :title="'New Template'">
      <div class="modal-body">
        <div class="content">
          <div class="form-group p-2">
            <label class="form-label" for="templateNameInput">Name</label>
            <input
              id="templateNameInput"
              name="name"
              class="form-input"
              type="text"
              placeholder="Name"
              pattern="^.{1,}$"
              required
              @keyup="$event.target.classList.remove('is-error')"
            >
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn btn-primary" @click="saveNewTemplate">
          Save
        </button>
        <button class="btn btn-link" @click="closeModal">
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
import {mapState} from 'vuex';


export default {
  name: 'Templates',
  components: {
    TemplateItem, Modal, PlusIcon
  },
  computed: mapState({
    templates: state => state.template.templates,
  }),
  methods: {
    openModal() {
      this.$refs.modal.open();
    },
    closeModal() {
      this.$refs.modal.close();
    },
    saveNewTemplate(event) {
      let templateNameInput = document.getElementById('templateNameInput');

      if (!templateNameInput.checkValidity()) {
        templateNameInput.classList.add('is-error');
        return;
      }
      event.target.classList.add('loading');

      let data = {
        name: templateNameInput.value
      };
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
};
</script>

<style scoped>
</style>
