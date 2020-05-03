<template>
  <div class="d-inline-block">
    <span class="h-sm" v-if="mode === 'view'" @click="mode = 'edit'">
      {{value}}
    </span>
    <div v-else-if="mode === 'edit'" class="input-group input-inline">
      <input type="text" v-model="value" class="form-input input-sm" :placeholder="placeholder">
      <button @click="onSave" class="btn btn-primary btn-sm input-group-btn">
        <check-icon size="16"></check-icon>
      </button>
      <button @click="mode = 'view'" class="btn btn-sm input-group-btn">
        <x-icon size="16"></x-icon>
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
        value: this.text
      }
    },
    methods: {
      onSave() {
        this.save(this.value);
        this.mode = 'view';
      }
    }
  }
</script>

<style scoped>

</style>
