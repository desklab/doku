<template>
  <modal ref="modal" class="modal-lg" v-bind:title="'Stylesheets'">
    <div class="modal-body">
      <div class="content">
        <StyleItem v-bind:stylesheet="baseStyle" v-bind:isBase="true"></StyleItem>
        <StyleItem v-for="style in stylesheets" v-bind:stylesheet="style" v-bind:isBase="false"></StyleItem>
      </div>
    </div>
    <div class="modal-footer">
      <button @click="close" class="btn btn-link">
        Close
      </button>
    </div>
  </modal>
</template>

<script>
  import Modal from "./Modal";
  import StyleItem from "./StyleItem";


  export default {
    name: 'StylesheetModal',
    components: {Modal, StyleItem},
    props: ['stylesheets', 'baseStyle'],
    methods: {
      toggle() {
        this.$refs.modal.toggle();
      },
      open() {
        this.$refs.modal.open();
      },
      close() {
        this.$refs.modal.close();
      }
    }
  }
</script>

<style scoped>

</style>
