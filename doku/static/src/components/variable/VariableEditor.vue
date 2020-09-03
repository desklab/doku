<template>
  <div class="doku-inline-var-code">
    <div class="doku-inline-var-controls">
      <animated-toggle v-if="!variable.is_list" ref="markdownToggle" v-bind:is-checked="variable.use_markdown">
        <template v-slot:on>Markdown</template>
        <template v-slot:off>Raw</template>
      </animated-toggle>
      <div class="form-inline">
        <input type="text" placeholder="CSS Class" class="form-input input-sm" ref="cssClassInput" :value="variable.css_class">
      </div>
    </div>
    <Editor ref="editor" v-bind:mode="'text/x-markdown'" v-bind:value="variable.content" v-bind:height="'auto'"></Editor>
  </div>
</template>

<script>
  import Editor from '../ui/Editor.vue';
  import AnimatedNotice from "../ui/AnimatedNotice";
  import AnimatedToggle from "../ui/AnimatedToggle";

  export default {
    name: 'VariableEditor',
    props: {
      variable: {
        type: Object
      },
      documentId: {
        type: Number,
        default: null
      }
    },
    components: {
      AnimatedToggle,
      AnimatedNotice,
      Editor,
    },
    data() {
      return {
        showCode: false,
        _showDone: false
      }
    },
    mounted() {
    },
    methods: {
      getValue() {
        return this.$refs.editor.getValue();
      },
      getCssClass() {
        return this.$refs.cssClassInput.value;
      },
      getUseMarkdown() {
        return this.$refs.markdownToggle.checked;
      },
      refresh() {
        this.$refs.editor.editor.refresh();
        this.$refs.editor.editor.focus();
      }
    }
  }
</script>

<style scoped>

</style>
