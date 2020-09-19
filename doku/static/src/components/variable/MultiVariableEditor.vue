<template>
  <div>
    <div class="doku-edit-vars">
      <folder-row :nested="true" name="Root" :always-open="true" :allow-add="true" :allow-remove="false" v-on:doku-dragend="onDrop($event, null)" v-on:doku-add-folder="addGroup">
        <div class="folder-list mb-2">
          <folder-row v-for="group in documentGroups" :name="group.name" :key="group.id" v-on:doku-dragend="onDrop($event, group.id)" :allow-add="false" :allow-remove="true" v-on:doku-remove-folder="removeGroup($event, group.id)">
            <inline-variable ref="vars" v-for="variable in group.variables.filter(v => v.parent == null)" :document-id="document.id" :key="variable.id" :variable="variable"></inline-variable>
          </folder-row>
        </div>
        <inline-variable ref="vars" v-for="variable in documentRootVariables.filter(v => v.parent == null)" :document-id="document.id" :key="variable.id" :variable="variable"></inline-variable>
      </folder-row>
    </div>
    <div class="editor-toolbar">
      <div class="ml-3">
        <div class="loading" v-if="loading"></div>
      </div>
      <animated-notice ref="toolbarNotice"></animated-notice>
      <div>
        <button ref="saveButton" @click="save" class="btn btn-primary">
          Save All
        </button>
      </div>
    </div>
    <Modal ref="confirmModal" class="modal-sm" title="Save All">
      <div class="modal-body">
        <div class="content">
          Do you really want to save all variables
        </div>
      </div>
      <div class="modal-footer">
        <animated-notice ref="modalNotice"></animated-notice>
        <button @click="save($event,true)" class="btn btn btn-primary">
          Save
        </button>
        <button @click="closeConfirmModal" class="btn btn-link">
          Close
        </button>
      </div>
    </Modal>
  </div>
</template>

<script>
  import InlineVariable from "./InlineVariable";
  import {mapActions, mapState, mapGetters} from "vuex";
  import Modal from "../ui/Modal";
  import * as actionTypes from '../../store/types/actions';
  import * as getterTypes from '../../store/types/getters';
  import AnimatedNotice from "../ui/AnimatedNotice";
  import FolderRow from "../ui/FolderRow";

  export default {
    name: 'MultiVariableEditor',
    components: {
      AnimatedNotice,
      Modal,
      InlineVariable,
      FolderRow
    },
    data() {
      return {
        _showNotice: false,
        _noticeText: '',
        _noticeClass: '',
        loading: false
      }
    },
    computed: {
      ...mapGetters('document', {
        documentGroups: getterTypes.DOCUMENT_GROUPS,
        documentRootVariables: getterTypes.DOCUMENT_ROOT_VARIABLES,
      }),
      ...mapState({document: state => state.document.document})
    },
    methods: {
      ...mapActions('variable', [
        actionTypes.UPDATE_VARIABLES,
      ]),
      ...mapActions('vargroup', [
        actionTypes.REMOVE_VARIABLE_GROUP,
        actionTypes.CREATE_VARIABLE_GROUP
      ]),
      closeConfirmModal() {
        this.$refs.confirmModal.close();
      },
      openConfirmModal() {
        this.$refs.confirmModal.open();
      },
      onDrop(event, group) {
        let variableId = event.dataTransfer.getData('variableId');
        this.updateVariables({id: variableId, group_id: group})
          .catch(console.error);
      },
      addGroup(event, name) {
        this.loading = true;
        this.createVariableGroup({
          document_id: this.document.id,
          name: name
        })
          .then(() => {
            this.$refs.toolbarNotice.trigger('Success!', 'text-dark');
          })
          .catch(err => {
            console.error(err);
            this.$refs.toolbarNotice.trigger('Error!', 'text-error');
          })
          .finally(() => {
            this.loading = false;
          });
      },
      removeGroup(event, groupId) {
        this.loading = true;
        this.removeVariableGroup(groupId)
          .then(() => {
            this.$refs.toolbarNotice.trigger('Success!', 'text-dark');
          })
          .catch(err => {
            console.error(err);
            this.$refs.toolbarNotice.trigger('Error!', 'text-error');
          })
          .finally(() => {
            this.loading = false;
          });
      },
      save(event, sure) {
        if (!sure) {
          this.openConfirmModal();
          return
        }
        event.target.classList.add('loading');
        let variables = [];
        if (Array.isArray(this.$refs.vars)) {
          variables.push(...this.$refs.vars.map(v => v.getData()));
        } else {
          variables.push(this.$refs.vars.getData());
        }
        this.updateVariables(variables)
          .then(() => {
            this.$refs.toolbarNotice.trigger('Success!', 'text-dark');
            this.closeConfirmModal();
          })
          .catch((err) => {
            console.error(err);
            this.$refs.modalNotice.trigger('Failed!', 'text-error');
          })
          .finally(() => {
            event.target.classList.remove('loading');
          });
      },
      updateEditors() {
        if (Array.isArray(this.$refs.vars)) {
          this.$refs.vars.forEach(v => v.updateEditor());
        } else {
          this.$refs.vars.updateEditor();
        }
      }
    }
  }
</script>

<style scoped>

</style>
