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
          <!-- Public/Private switch
          <div class="form-group p-2">
            <label class="form-switch">
              <input checked name="public" id="documentPublicInput" type="checkbox">
              <i class="form-icon"></i> Make document public
            </label>
          </div>
          -->
          <div class="form-group p-2">
            <label class="form-label" for="documentTemplateSelect">Template</label>        
            <div class="border rounded-lg mt-2 p-4">
              <span class="d-block mb-3" v-if="selectedTemplate !== null && selectedTemplate !== undefined">
                Template: <b>{{ selectedTemplate.name }}</b>
              </span>
              <span class="d-block mb-3" v-if="selectedTemplate === null || selectedTemplate === undefined">
                Template: <b>None / Create New</b>
              </span>
              <button @click="$refs.selectModal.open()" class="btn btn-sm">Select Template</button>
              <button @click="selectNone" class="btn btn-sm">Select None / Create New</button>
              <select-modal :none="false" ref="selectModal" title="Select Template" v-on:doku-selection-made="saveTemplateSelection" :apiFetch="templateApiFetch"></select-modal>
            </div>

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
  import Modal from '../components/ui/modal/Modal.vue';
  import BulkDownload from '../components/ui/modal/BulkDownload.vue';
  import selectModal from '../components/ui/modal/SelectModal';

  export default {
    name: 'home',
    components: {
      Modal, PlusIcon, DownloadIcon, BulkDownload, selectModal
    },
    data() {
      return {
        selectedTemplate: null,
        templates: [],
        templateApiFetch: templateApi.fetchTemplates
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
        //let documentPublicInput = document.getElementById('documentPublicInput');

        if (!documentNameInput.checkValidity()) {
          documentNameInput.classList.add('is-error');
          return;
        }
        event.target.classList.add('loading');
        let template_id = this.selectedTemplateId;
        let data = {
          name: documentNameInput.value,
          public: true, //documentPublicInput.checked,
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
      },
      saveTemplateSelection(template) {
        this.selectedTemplate = template;
      },
      selectNone() {
        this.selectedTemplate = null;
      }
    }
  }
</script>

<style scoped>

</style>
