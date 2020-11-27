<template>
  <div class="doku-inline-var">
    <variable-editor :variable="variable" />
  </div>
</template>

<script>
import VariableEditor from '../components/document/VariableEditor';
export default {
  name: 'Snippet',
  components: {
    VariableEditor
  },
  data() {
    return {
      variable: window.snippetObj
    };
  }
};
</script>

<style scoped>

</style>
