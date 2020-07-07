<template>
  <div class="doku-document-toolbar">
    <h3 class="m-0">Documents</h3>
    <div>
      <button @click="openModal" class="btn btn-sm">
        <plus-icon size="18"></plus-icon>
        Create new document
      </button>
      <button @click="openDownloadModal" class="btn btn-sm">
        <download-icon size="18"></download-icon>
        Bulk Download
      </button>
    </div>
    <bulk-download ref="downloadModal"></bulk-download>
    <modal ref="modal" v-bind:title="'New Document'">
      <div class="modal-body">
        <div class="content">
          <div class="form-group p-2">
            <label class="form-label" for="documentNameInput">Name</label>
            <input v-on:keyup="$event.target.classList.remove('is-error')" name="name" class="form-input" type="text" id="documentNameInput" placeholder="Name" pattern="^.{1,}$" required>
          </div>
          <div class="form-group p-2">
            <label class="form-switch">
              <input checked name="public" id="documentPublicInput" type="checkbox">
              <i class="form-icon"></i> Make document public
            </label>
          </div>
          <div class="form-group p-2">
            <label class="form-label" for="documentTemplateSelect">Template</label>
            <select id="documentTemplateSelect" name="template" class="form-select">
              <option value="">Create new</option>
              <option v-for="template in templates" :value="template.id" :key="template.id">{{ template.name }}</option>
            </select>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button @click="save" class="btn btn btn-primary">
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
  import {PlusIcon, DownloadIcon} from 'vue-feather-icons';

  import templateApi from '../api/template';
  import documentApi from '../api/document';
  import Modal from '../components/ui/Modal.vue';
  import BulkDownload from '../components/ui/BulkDownload.vue';

  export default {
    name: 'home',
    components: {
      Modal, PlusIcon, DownloadIcon, BulkDownload
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
      openDownloadModal() {
        this.$refs.downloadModal.open();
      },
      closeModal() {
        this.$refs.modal.close();
      },
      save(event) {
        let documentNameInput = document.getElementById('documentNameInput');
        let documentPublicInput = document.getElementById('documentPublicInput');
        let documentTemplateSelect = document.getElementById('documentTemplateSelect');

        if (!documentNameInput.checkValidity()) {
          documentNameInput.classList.add('is-error');
          return;
        }
        event.target.classList.add('loading');
        let template_id = documentTemplateSelect.value;
        let data = {
          name: documentNameInput.value,
          public: documentPublicInput.checked,
          template_id: (template_id === "") ? null : template_id
        }
        documentApi.createDocument(data)
          .then((response) => {
            window.location.href = response.data.public_url;
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
