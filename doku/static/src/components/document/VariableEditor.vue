<template>
  <div class="doku-inline-var-code">
    <div class="doku-inline-var-controls">
      <animated-toggle v-if="!variable.is_list" ref="markdownToggle"
                       input-name="use_markdown" :is-checked="variable.use_markdown"
      >
        <template #on>
          Markdown
        </template>
        <template #off>
          Raw
        </template>
      </animated-toggle>
      <!--
        The slot is used to extend the editor by providing
        additional buttons and actions
      -->
      <slot />
      <div class="form-inline">
        <input ref="cssClassInput" type="text" placeholder="CSS Class"
               class="form-input input-sm" name="css_class" :value="variable.css_class"
        >
      </div>
    </div>
    <Editor
      ref="editor" :mode="'text/x-markdown'" input-name="content"
      :value="variable.content" :height="'auto'"
    />
  </div>
</template>

<script>
import Editor from '../ui/Editor.vue';
import AnimatedToggle from '../ui/form/AnimatedToggle';

export default {
  name: 'VariableEditor',
  components: {
    AnimatedToggle,
    Editor,
  },
  props: {
    variable: {
      type: Object,
      default: undefined
    },
    documentId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      showCode: false,
    };
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
};
</script>

<style scoped>

</style>
