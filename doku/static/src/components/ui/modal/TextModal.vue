<template>
  <modal ref="modal" :title="title">
    <div class="modal-body">
      <div class="content">
        <div class="form-group p-2">
          <label class="form-label" for="textInput">Name</label>
          <input id="textInput" name="name" class="form-input" type="text" pattern="^.{1,}$" required @keyup="$event.target.classList.remove('is-error')">
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-link" @click="save">
        Save
      </button>
    </div>
  </modal>
</template>

<script>
import Modal from './Modal';
import AnimatedNotice from '../AnimatedNotice';

/**
 * Text Modal
 *
 * Modal used to request a text value from the user (e.g. name for 
 * new object when using 'Save as new Template'). 
 *
 * @param {String} title - Passed to the modal component.
 *
 * @event doku-text-entered: Passes the text input when the modal is closed.
 */

export default {
  name: 'TextModal',
  components: {
    Modal, 
    AnimatedNotice
  },
  props: {
    title: String
  },
  data() {
    return {
      loaded: {}
    };
  },
  methods: {
    toggle() {
      this.$refs.modal.toggle();
    },
    open() {
      this.$refs.modal.open();
    },
    close() {
      this.$refs.modal.close();
    },
    save() {
      this.close();
      textInput = document.getElementById('textInput');
      this.$emit('doku-text-entered', textInput.value);
    }
  }
};
</script>

<style scoped>

</style>
