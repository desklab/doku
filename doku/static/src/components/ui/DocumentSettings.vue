<template>
  <div>
    <div class="doku-edit-settings">
      <div class="container grid-md">
        <div class="columns">
          <div class="card col-12">
            <div class="card-header">
              <h5 class="card-title h5">Document Settings</h5>
              <div class="card-subtitle text-dark">Document <b>{{document.name}}</b></div>
            </div>
            <div class="card-body">
              <div class="form-group form-inline">
                <label class="form-label" for="documentNameInput"><b>Name</b></label>
                <input class="form-input" type="text" id="documentNameInput" name="name" :value="document.name" placeholder="Name">
              </div>
              <div class="form-group mt-2">
                <animated-toggle ref="documentPublicInput" v-bind:is-checked="document.public">
                  <template v-slot:on>Public</template>
                  <template v-slot:off>Private</template>
                </animated-toggle>
              </div>
              <div class="form-group mt-2 form-inline">
                <label class="form-label" for="documentTemplateSelect"><b>Change Template</b></label>
                <select id="documentTemplateSelect" name="template" class="form-select">
                  <option v-for="template in templates" :value="template.id" :key="template.id">{{ template.name }}</option>
                </select>
              </div>
            </div>
            <div class="card-footer">
              <button class="btn btn-primary float-right" @click="save">Save</button>
              <animated-notice class="float-right" ref="saveNotice"></animated-notice>
            </div>
          </div>
          <div class="card col-12 mt-3 border-error">
            <div class="card-header">
              <h5 class="card-title h5 text-dark">Remove</h5>
              <div class="card-subtitle text-dark">Permanently delete <b>{{document.name}}</b></div>
            </div>
            <div class="card-body">
              <div class="toast toast-warning bg-warning-light text-dark">
                <info-icon size="1x" class="text"></info-icon>
                <b>Notice</b><br>
                Removing the document will permanently delete all variables
                associated with it.
                However, templates and stylesheets will continue
                to be available for other documents.
              </div>
            </div>
            <div class="card-footer">
              <button class="btn btn-error float-right" @click="$refs.removeConfirmation.open()">Remove</button>
              <animated-notice class="float-right" ref="deleteNotice"></animated-notice>
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
  import RemoveDocumentConfirmation from "./RemoveDocumentConfirmation.vue";

  export default {
    name: 'VariableEditor',
    components: {
      AnimatedNotice, InfoIcon,
      Modal, AnimatedToggle,
      RemoveDocumentConfirmation
    },
    computed: mapState({
      document: state => state.document.document
    }),
    data() {
      return {
        templates: []
      }
    },
    mounted() {
      templateApi.fetchTemplates()
        .then((response) =>{
          this.templates = response.data;
        })
        .catch(console.error);
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
          template_id: documentTemplateSelect.value
        };
        console.log(data);
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
      }
    }
  }
</script>

<style scoped>

</style>
