<template>
  <div class="editor"></div>
</template>

<script>
  import CodeMirror from 'codemirror/lib/codemirror';
  import 'codemirror/lib/codemirror.css';
  import 'codemirror/theme/base16-light.css';
  import 'codemirror/addon/hint/show-hint.js';
  import 'codemirror/addon/hint/show-hint.css';
  import 'codemirror/addon/hint/html-hint';
  import 'codemirror/addon/hint/anyword-hint';
  import 'codemirror/mode/htmlmixed/htmlmixed.js';
  import 'codemirror/mode/markdown/markdown.js';

  export default {
    name: 'Editor',
    props: {
      value: {
        default: '',
        type: String
      },
      height: {
        default: '100%'
      },
      width: {
        default: '100%'
      },
      mode: {
        default: 'text/html',
        type: String
      }
    },
    mounted() {
      this.editor = CodeMirror(this.$el, {
        mode: this.mode,
        value: this.value,
        theme: 'base16-light',
        readOnly: false,
        autofocus: true,
        lineNumbers: true,
        tabSize: 2,
        lineWrapping: true,
        extraKeys: {"Ctrl-Space": "autocomplete"}
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
  }
</script>

<style scoped>

</style>
