<template>
  <modal ref="modal" class="modal-md" title="Remove Document">
    <div class="modal-body">
      <div class="content">
        <div class="toast toast-warning bg-warning-light text-dark">
          <b>Notice</b><br>
          Removing the document will permanently delete all variables
          associated with it.
          However, templates and stylesheets will continue to be
          available for other documents.
        </div>
        <br>
        Please confirm that you want to remove this document!
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-link float-right" @click="close">
        Abort
      </button>
      <button class="btn btn-error float-right mr-1" @click="remove">
        Remove Document
      </button>
    </div>
  </modal>
</template>

<script>
import Modal from '../ui/modal/Modal';
import {mapActions} from 'vuex';
import * as actionTypes from '../../store/types/actions';
import * as ns from '../../store/namespace';

export default {
  name: 'RemoveDocumentConfirmation',
  components: {Modal},
  methods: {
    ...mapActions(ns.DOCUMENT, [
      actionTypes.REMOVE_DOCUMENT
    ]),
    remove() {
      this.$refs.modal.close();
      this.$emit('remove-confirmed');
    },
    close() {
      this.$refs.modal.close();
    },
    open() {
      this.$refs.modal.open();
    },
  }
};
</script>

<style scoped>

</style>
