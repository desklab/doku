<template>
  <div>
    <div class="doku-edit-vars">
      <div class="folder-list mb-2">
        <folder-row v-for="group in document.variable_groups" :name="group.name" :key="group.id">
          <InlineVariable ref="vars" v-for="variable in group.variables.filter(v => v.parent == null)" :document-id="document.id" :key="variable.id" :variable="variable" draggable="true" @dragstart='startDrag($event, variable)'></InlineVariable>
        </folder-row>
      </div>
      <InlineVariable ref="vars" v-for="variable in document.root_variables.filter(v => v.parent == null)" :document-id="document.id" :key="variable.id" :variable="variable" draggable="true" @dragstart='startDrag($event, variable)'></InlineVariable>
    </div>
    <div class="editor-toolbar">
      <span></span>
      <div>
        <AnimatedNotice ref="toolbarNotice"></AnimatedNotice>
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
        <AnimatedNotice ref="modalNotice"></AnimatedNotice>
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
  import {mapActions, mapState} from "vuex";
  import Modal from "../ui/Modal";
  import * as actionTypes from '../../store/types/actions';
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
        _noticeClass: ''
      }
    },
    computed: mapState({
      document: state => state.document.document,
      variables: state => state.variable.variables,
    }),
    methods: {
      ...mapActions('variable', [
        actionTypes.UPDATE_VARIABLES,
      ]),
      closeConfirmModal() {
        this.$refs.confirmModal.close();
      },
      openConfirmModal() {
        this.$refs.confirmModal.open();
      },
      startDrag(event, variable) {

      },
      onDrop(event, group) {

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
