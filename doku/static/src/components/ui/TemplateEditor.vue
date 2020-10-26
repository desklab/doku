<template>
  <div>
    <Editor :value="template.source" class="editor" ref="editor"></Editor>
    <div class="editor-toolbar">
      <button @click="$refs.stylesSelector.open()" class="btn btn-sm">Styles</button>
      <div>
        <AnimatedNotice ref="saveNotice"></AnimatedNotice>
        <button ref="saveButton" @click="save" class="btn btn-primary">
          Save
        </button>
      </div>
    </div>
    <multi-select-modal ref="stylesSelector" title="Select Stylesheets" :api-fetch="stylesheetApiFetch" :defaultSelection="stylesheets" :none="false" :editLink="'../stylesheets'" v-on:doku-selection-made="setSelectedStylesheets"></multi-select-modal>
  </div>
</template>

<script>
  import MultiSelectModal from "./MultiSelectModal";
  import {mapActions, mapState} from "vuex";
  import Editor from "./Editor";
  import * as actionTypes from '../../store/types/actions';
  import AnimatedNotice from "./AnimatedNotice";
  import stylesheetApi from '../../api/stylesheet';

  export default {
    name: 'TemplateEditor',
    props: {
      _showDone: false
    },
    components: {
      AnimatedNotice,
      MultiSelectModal, 
      Editor
    },
    data() {
      return {
        stylesheetApiFetch: stylesheetApi.fetchStylesheets
      }
    },
    computed: mapState({
      template: state => state.template.template,
      stylesheets: state => state.stylesheet.stylesheets
    }),
    methods: {
      ...mapActions('template', [
        actionTypes.UPDATE_TEMPLATE,
      ]),
      ...mapActions('stylesheet', [
        actionTypes.SET_STYLESHEETS_FOR_TEMPLATE,
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
      setSelectedStylesheets(selectedIDs) {
        this.setStylesheets(selectedIDs);
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
