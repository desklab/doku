<template>
  <div>
    <Editor :value="template.source" class="editor" ref="editor"></Editor>
    <div class="editor-toolbar">
      <button @click="$refs.stylesSelector.open()" class="btn btn-sm">Styles</button>
      <div>
        <AnimatedNotice ref="saveNotice"></AnimatedNotice>
        <button ref="saveButton" @click="$refs.saveAsNewNameInput.open()" class="btn btn-primary">
          Save as new Template
        </button>
        <button ref="saveButton" @click="save" class="btn btn-primary">
          Save
        </button>
        <a class="btn ml-2 tooltip tooltip-left" href="./../template" data-tooltip="Unsaved changes will be discarded!">Close</a>
      </div>
    </div>
    <multi-select-modal ref="stylesSelector" title="Select Stylesheets" :api-fetch="stylesheetApiFetch" :defaultSelection="selectedStylesheets" :none="false" :editLink="'../stylesheets'" v-on:doku-selection-made="setSelectedStylesheets"></multi-select-modal>
    <text-modal ref="saveAsNewNameInput" title="Save as new Template" v-on:doku-text-entered="saveAsNew"></text-modal>
  </div>
</template>

<script>
  import TextModal from "../ui/modal/TextModal";
  import MultiSelectModal from "../ui/modal/MultiSelectModal";
  import {mapActions, mapState} from "vuex";
  import Editor from "../ui/Editor";
  import * as actionTypes from '../../store/types/actions';
  import AnimatedNotice from "../ui/AnimatedNotice";
  import stylesheetApi from '../../api/stylesheet';
  import templateApi from '../../api/template';

  export default {
    name: 'TemplateEditor',
    props: {
      _showDone: false
    },
    components: {
      AnimatedNotice,
      MultiSelectModal,
      TextModal,
      Editor
    },
    data() {
      return {
        stylesheetApiFetch: stylesheetApi.fetchStylesheets
      }
    },
    computed: {
      ...mapState({
        template: state => state.template.template
      }),
      selectedStylesheets: function () {
        let stylesheetIDs = [];
        for (let i in this.template.styles) {
          stylesheetIDs.push(this.template.styles[i].id);
        }
        return stylesheetIDs;
      }
    },
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
      saveAsNew(newName){
        if (event !== undefined) {
          event.target.classList.add('loading');
        }
        let data = {
          name: newName,
          source: this.$refs.editor.getValue()
        }
        console.log(data)
        templateApi.createTemplate(data)
          .then((response) => {
            window.location.href = response.data.id;
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
        let selectedStylesheetObjects = [];
        for (let i in selectedIDs) {
          selectedStylesheetObjects.push({
            id: selectedIDs[i]
          });
        }
        this.updateTemplate({
          id: this.template.id,
          styles: selectedStylesheetObjects
        })
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
