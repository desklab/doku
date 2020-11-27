<template>
  <div class="d-inline-block">
    <span v-if="mode === 'view'" @click="edit">
      {{ text }}
    </span>
    <div v-else class="input-group input-inline">
      <input
        v-model="value"
        :placeholder="placeholder"
        class="form-input input-sm"
        type="text"
      >
      <button class="btn btn-primary btn-sm input-group-btn"
              :disabled="value.replaceAll(' ','').length < 1"
              @click="onSave"
      >
        <check-icon size="16" />
      </button>
      <button class="btn btn-sm input-group-btn" @click="abort">
        <x-icon size="16" />
      </button>
    </div>
  </div>
</template>

<script>
import {XIcon, CheckIcon} from 'vue-feather-icons';

export default {
  name: 'TextEdit',
  components: {
    CheckIcon, XIcon
  },
  props: {
    text: {
      type: String
    },
    placeholder: {
      type: String
    },
    save: {
      type: Function
    }
  },
  data() {
    return {
      // Possible modes: 'edit' and 'view'
      mode: 'view',
      // As text is a property, we try to not mutate it as part of
      // changing the value.
      value: this.text,
    };
  },
  methods: {
    onSave() {
      this.save(this.value);
      // The variable text should be updated by the parent component
      // that will update the supplied property using the callback.
      this.mode = 'view';
    },
    abort() {
      this.mode = 'view';
      this.$nextTick(() => {
        // Change the value after updating the UI. This will avoid
        // redrawing the input to change text before hiding it anyway.
        this.value = this.text;
      });
    },
    edit() {
      this.value = this.text;
      this.mode = 'edit';
    }
  }
};
</script>

<style scoped>

</style>
