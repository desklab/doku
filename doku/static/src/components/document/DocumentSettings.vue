<template>
  <div>
    <div class="doku-edit-settings mx-4 mt-4">
      <div class="container grid-xl">
        <div class="columns">
          <div class="col-12">
            <h5 class="border-bottom pb-2">
              Document Settings
            </h5>
            <div class="d-block">
              <div class="form-group form-inline">
                <label class="form-label" for="documentNameInput">
                  <b>Name</b>
                  <small><animated-notice ref="saveNotice" class="ml-1" /></small>
                </label>
                <div class="input-group">
                  <input id="documentNameInput" class="form-input"
                         type="text" name="name"
                         :value="document.name" placeholder="Name"
                  >
                  <button class="btn input-group-btn" @click="save">
                    Save
                  </button>
                </div>
              </div>
            </div>
            <div class="border rounded-lg mt-2 p-4">
              <span class="d-block mb-3">
                Current Template: <b>{{ document.template.name }}</b>
              </span>
              <button class="btn btn-sm" @click="$refs.selectModal.open()">
                Change Template
              </button>
              <a :href="`/template/`" class="btn btn-sm btn-link">Manage Templates</a>
              <select-modal ref="selectModal" :none="false"
                            title="Select Template"
                            :default-selection="selectedTemplate"
                            :api-fetch="apiFetch"
                            @doku-selection-made="saveSelection"
              />
            </div>
          </div>

          <div class="col-12 mt-8">
            <h5 class="border-bottom pb-2">
              Other Settings
            </h5>
            <div class="tile p-4 border border-error rounded-lg">
              <div class="tile-content">
                <h5 class="tile-title mb-0">
                  Remove
                </h5>
                <small class="tile-subtitle mb-0">
                  Permanently delete <b>{{ document.name }}</b>.
                  This will also delete all variables associated with it.
                </small>
              </div>
              <div class="tile-action">
                <animated-notice ref="deleteNotice" class="float-right" />
                <button class="btn btn-error btn-sm"
                        @click="$refs.removeConfirmation.open()"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <remove-document-confirmation ref="removeConfirmation" @remove-confirmed="remove" />
  </div>
</template>

<script>
import {mapActions, mapState} from 'vuex';

import * as actionTypes from '../../store/types/actions';
import templateApi from '../../api/template';
import * as ns from '../../store/namespace';
import AnimatedNotice from '../ui/AnimatedNotice';
import SelectModal from '../ui/modal/SelectModal.vue';
import RemoveDocumentConfirmation from './RemoveDocumentConfirmation.vue';

export default {
  name: 'DocumentSettings',
  components: {
    AnimatedNotice,
    RemoveDocumentConfirmation,
    SelectModal
  },
  data() {
    return {
      selectedTemplate: null,
      apiFetch: templateApi.fetchTemplates
    };
  },
  computed: mapState({
    document: state => state.document.document
  }),
  mounted() {
    this.selectedTemplate = this.document.template;
  },
  methods: {
    ...mapActions(ns.DOCUMENT, [
      actionTypes.REMOVE_DOCUMENT,
      actionTypes.UPDATE_DOCUMENT
    ]),
    save(event) {
      event.target.classList.add('loading');
      let documentNameInput = document.getElementById('documentNameInput');
      let data = {
        id: this.document.id,
        name: documentNameInput.value,
      };
      this.updateDocument(data)
        .then(() => {
          this.$refs.saveNotice.trigger('Success!', 'text-primary');
        })
        .catch((err) => {
          console.error(err);
          this.$refs.saveNotice.trigger('Failed! ' + err.message, 'text-error');
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
          this.$refs.deleteNotice.trigger('Failed! ' + err.message, 'text-error');
          event.target.classList.remove('loading');
        });
    },
    saveSelection(selection) {
      this.selectedTemplate = selection;
      let data = {
        id: this.document.id,
        template_id: this.selectedTemplate.id,
        includes: ['template']
      };
      this.updateDocument(data)
        .catch((err) => {
          console.error(err);
        });
    }
  }
};
</script>

<style scoped>

</style>
