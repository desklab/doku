<template>
  <modal ref="modal" class="modal-md" v-bind:title="'Remove Document'">
    <div class="modal-body">
      <div class="content">
        <div class="toast toast-warning bg-warning-light text-dark">
          <b>Notice</b><br>
          Removing the document will permanently delete all variables associated with it.
          However, templates and stylesheets will continue to be available for other documents.
        </div>  
        <br>
        Please confirm that you want to remove this document!
      </div>
    </div>
    <div class="modal-footer">
      <button @click="close" class="btn btn-link float-right">
        Abort 
      </button>
      <button @click="remove" class="btn btn-error float-right mr-1">
        Remove Document
      </button>
    </div>
  </modal>
</template>

<script>
  import Modal from "./Modal";
  import {mapActions, mapState} from "vuex";
  import * as actionTypes from "../../store/types/actions";
  import * as ns from '../../store/namespace';

  export default {
    name: 'RemoveDocumentConfirmation',
    components: {Modal},
    methods: {
      ...mapActions(ns.DOCUMENT, [
        actionTypes.REMOVE_DOCUMENT
      ]),
      remove(event) {
        this.$refs.modal.close();
        this.$emit('remove-confirmed')
      },
      close() {
        this.$refs.modal.close();
      },
      open() {
        this.$refs.modal.open();
      },
    }
  }
</script>

<style scoped>

</style>
