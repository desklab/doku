<template>
  <div class="doku-document-toolbar">
    <h3 class="m-0">
      Documents
    </h3>
    <div>
      <button class="btn btn-sm" @click="openModal">
        <plus-icon size="18" />
        Create new document
      </button>
      <button class="btn btn-sm" @click="openDownloadModal">
        <download-icon size="18" />
        Bulk Download
      </button>
    </div>
    <bulk-download ref="downloadModal" />
    <modal ref="modal" :title="'New Document'">
      <div class="modal-body">
        <div class="content">
          <div class="form-group p-2">
            <label class="form-label" for="documentNameInput">Name</label>
            <input
              id="documentNameInput"
              name="name"
              class="form-input"
              type="text"
              placeholder="Name"
              pattern="^.{1,}$"
              required
              @keyup="$event.target.classList.remove('is-error')"
            >
          </div>
          <div class="form-group p-2">
            <label class="form-label">Template</label>
            <div class="border rounded-lg mt-2 p-4">
              <span v-if="selectedTemplate !== null || selectedTemplate !== undefined"
                    class="d-block mb-3"
              >
                Template: <b>{{ selectedTemplate.name }}</b>
              </span>
              <span v-else class="d-block mb-3">
                Template: <b>None / Create New</b>
              </span>
              <button class="btn btn-sm" @click="$refs.selectModal.open()">
                Select Template
              </button>
              <button class="btn btn-sm" @click="selectNone">
                Select None / Create New
              </button>
              <select-modal
                ref="selectModal"
                :none="false"
                title="Select Template"
                :api-fetch="templateApiFetch"
                @doku-selection-made="saveTemplateSelection"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn btn-primary" @click="save">
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
import {PlusIcon, DownloadIcon} from 'vue-feather-icons';

import templateApi from '../api/template';
import documentApi from '../api/document';
import Modal from '../components/ui/modal/Modal.vue';
import BulkDownload from '../components/ui/modal/BulkDownload.vue';
import selectModal from '../components/ui/modal/SelectModal';

export default {
  name: 'Home',
  components: {
    Modal, PlusIcon, DownloadIcon, BulkDownload, selectModal
  },
  data() {
    return {
      selectedTemplate: null,
      templates: [],
      templateApiFetch: templateApi.fetchTemplates
    };
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
      if (!documentNameInput.checkValidity()) {
        documentNameInput.classList.add('is-error');
        return;
      }
      event.target.classList.add('loading');
      let template_id = this.selectedTemplateId;
      let data = {
        name: documentNameInput.value,
        public: true, //documentPublicInput.checked,
        template_id: (template_id === '') ? null : template_id
      };
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
};
</script>

<style scoped>

</style>
