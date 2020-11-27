<template>
  <div class="editor">
    <!-- eslint-disable-next-line vue/no-textarea-mustache -->
    <textarea ref="editorTextArea" :name="inputName">{{ value }}</textarea>
  </div>
</template>

<script>
import { CodeMirror } from 'codemirror/src/edit/main.js';
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/base16-light.css';
import xml from '../../codemirror/xml';
import markdown from '../../codemirror/markdown';

xml(CodeMirror);
markdown(CodeMirror);

export default {
  name: 'Editor',
  props: {
    value: {
      default: '',
      type: String
    },
    height: {
      type: String,
      default: '100%'
    },
    width: {
      type: String,
      default: '100%'
    },
    mode: {
      default: 'text/html',
      type: String
    },
    inputName: {
      default: 'content',
      type: String,
    }
  },
  mounted() {
    this.editor = CodeMirror.fromTextArea(this.$refs.editorTextArea, {
      mode: this.mode,
      value: this.value,
      theme: 'base16-light',
      readOnly: false,
      autofocus: true,
      lineNumbers: true,
      tabSize: 2,
      lineWrapping: true,
      extraKeys: {'Ctrl-Space': 'autocomplete'}
    });
    this.editor.setSize(this.width, this.height);
  },
  methods: {
    getValue: function () {
      if (this.editor !== undefined && this.editor !== null) {
        return this.editor.getValue();
      } else {
        return this.value;
      }
    }
  }
};
</script>

<style scoped>

</style>
