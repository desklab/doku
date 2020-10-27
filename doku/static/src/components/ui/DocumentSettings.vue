<template>
  <div>
    <div class="doku-edit-settings mx-4 mt-4">
      <div class="container grid-xl">
        <div class="columns">
          <div class="col-12">
            <h5 class="border-bottom pb-2">Document Settings</h5>
            <div class="d-block">
              <div class="form-group form-inline">
                <label class="form-label" for="documentNameInput"><b>Name</b></label>
                <div class="input-group">
                  <input class="form-input" type="text" id="documentNameInput" name="name" :value="document.name" placeholder="Name">
                  <button class="btn input-group-btn" @click="save">Save</button>
                </div>
              </div>
            </div>
            <div class="border rounded-lg mt-2 p-4">
              <span class="d-block mb-3">
                Current Template: <b>{{ document.template.name }}</b>
              </span>
              <button @click="$refs.selectModal.open()" class="btn btn-sm">Change Template</button>
              <a :href="`/template/${document.template.id}`" class="btn btn-sm btn-link">Edit Template</a>
              <select-modal :none="false" ref="selectModal" title="Select Template" :defaultSelection="selectedTemplate" v-on:doku-selection-made="saveSelection" :apiFetch="apiFetch"></select-modal>
            </div>
            <!-- Public/Private switch
            <div class="form-group mt-2">
              <animated-toggle ref="documentPublicInput" v-bind:is-checked="document.public">
                <template v-slot:on>Public</template>
                <template v-slot:off>Private</template>
              </animated-toggle>
            </div>
            -->
          </div>

          <div class="col-12 mt-8">
            <h5 class="border-bottom pb-2">Other Settings</h5>
            <div class="tile p-4 border border-error rounded-lg">
              <div class="tile-content">
                <h5 class="tile-title mb-0">Remove</h5>
                <small class="tile-subtitle mb-0">
                  Permanently delete <b>{{document.name}}</b>.
                  This will also delete all variables associated with it.
                </small>
              </div>
              <div class="tile-action">
                <animated-notice class="float-right" ref="deleteNotice"></animated-notice>
                <button class="btn btn-error btn-sm" @click="$refs.removeConfirmation.open()">Remove</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <remove-document-confirmation ref="removeConfirmation" @remove-confirmed="remove"></remove-document-confirmation>
  </div>
</template>

<script>
  import {mapActions, mapState} from "vuex";
  import {InfoIcon} from 'vue-feather-icons';

  import AnimatedToggle from './AnimatedToggle';
  import Modal from "./Modal";
  import * as actionTypes from '../../store/types/actions';
  import templateApi from '../../api/template';
  import * as ns from '../../store/namespace';
  import AnimatedNotice from "./AnimatedNotice";
  import SelectModal from './SelectModal.vue';
  import RemoveDocumentConfirmation from "./RemoveDocumentConfirmation.vue";

  export default {
    name: 'DocumentSettings',
    components: {
      AnimatedNotice, InfoIcon,
      Modal, AnimatedToggle,
      RemoveDocumentConfirmation,
      SelectModal
    },
    computed: mapState({
      document: state => state.document.document
    }),
    data() {
      return {
        selectedTemplate: null,
        apiFetch: templateApi.fetchTemplates
      }
    },
    mounted() {
      this.selectedTemplate = this.document.template.id;
    },
    methods: {
      ...mapActions(ns.DOCUMENT, [
        actionTypes.REMOVE_DOCUMENT,
        actionTypes.UPDATE_DOCUMENT
      ]),
      save(event) {
        event.target.classList.add('loading');
        let documentNameInput = document.getElementById('documentNameInput');
        let documentTemplateSelect = document.getElementById('documentTemplateSelect');
        let data = {
          id: this.document.id,
          name: documentNameInput.value,
          public: this.$refs.documentPublicInput.checked,
          template_id: this.selectedTemplate
        };
        this.updateDocument(data)
          .then(() => {
            this.$refs.saveNotice.trigger('Success!', 'text-dark');
          })
          .catch((err) => {
            console.error(err);
            this.$refs.saveNotice.trigger('Failed!', 'text-error');
          })
          .finally(() => {
            event.target.classList.remove('loading');
          });
      },
      remove(event) {
        this.removeDocument(this.document.id)
          .then(() => {window.location.href = '/';})
          .catch((err) => {
            console.error(err);
            this.$refs.deleteNotice.trigger('Failed!', 'text-error');
            event.target.classList.remove('loading');
          });
      },
      saveSelection(id) {
        this.selectedTemplate = id;
      }
    }
  }
</script>

<style scoped>

</style>
