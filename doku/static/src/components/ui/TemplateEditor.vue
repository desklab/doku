<template>
  <div>
    <Editor :value="template.source" class="editor" ref="editor"></Editor>
    <div class="editor-toolbar">
      <button @click="$refs.stylesModal.open()" class="btn btn-sm">Styles</button>
      <div>
        <AnimatedNotice ref="saveNotice"></AnimatedNotice>
        <button ref="saveButton" @click="save" class="btn btn-primary">
          Save
        </button>
      </div>
    </div>
    <StylesheetModal v-bind:stylesheets="stylesheets" v-bind:base-style="template.base_style" ref="stylesModal"></StylesheetModal>
  </div>
</template>

<script>
  import StylesheetModal from "./StylesheetModal";
  import {mapActions, mapState} from "vuex";
  import Editor from "./Editor";
  import * as actionTypes from '../../store/types/actions';
  import AnimatedNotice from "./AnimatedNotice";

  export default {
    name: 'TemplateEditor',
    props: {
      _showDone: false
    },
    components: {
      AnimatedNotice,
      StylesheetModal, Editor
    },
    computed: mapState({
      template: state => state.template.template,
      stylesheets: state => state.stylesheet.stylesheets
    }),
    methods: {
      ...mapActions('template', [
        actionTypes.UPDATE_TEMPLATE,
      ]),
      save(event) {
        if (event !== undefined) {
          event.target.classList.add('loading');
        }
        this.updateTemplate({
          id: this.template.id,
          source: this.$refs.editor.getValue()
        })
          .then(() => {
            this.$refs.saveNotice.trigger('Success!', 'text-dark');
          })
          .catch((err) => {
            console.error(err);
            this.$refs.saveNotice.trigger('Failed!', 'text-error');
          })
          .finally(() => {
            if (event !== undefined) {
              event.target.classList.remove('loading');
            }
          });
      },
      updateEditor() {
        this.$refs.editor.editor.refresh();
        this.$refs.editor.editor.focus();
      }
    }
  }
</script>

<style scoped>

</style>
