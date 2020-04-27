<template>
  <div>
    <Editor :value="document.template.source" class="editor" ref="editor"></Editor>
    <div class="editor-toolbar">
      <button @click="$refs.stylesModal.open()" class="btn btn-sm">Styles</button>
      <div>
        <AnimatedNotice ref="saveNotice"></AnimatedNotice>
        <button ref="saveButton" @click="save" class="btn btn-primary">
          Save
        </button>
      </div>
    </div>
    <StylesheetModal v-bind:stylesheets="document.template.styles" v-bind:base-style="document.template.base_style" ref="stylesModal"></StylesheetModal>
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
      document: state => state.document.document
    }),
    methods: {
      ...mapActions('document', [
        actionTypes.UPDATE_DOCUMENT_TEMPLATE,
      ]),
      save(event) {
        event.target.classList.add('loading');
        this.updateDocumentTemplate({
          id: this.document.template.id,
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
            event.target.classList.remove('loading');
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
