<template>
  <div>
    <Editor ref="editor" :value="template.source" class="editor" />
    <div class="editor-toolbar">
      <button class="btn btn-sm" @click="$refs.stylesSelector.open()">
        Styles
      </button>
      <div>
        <AnimatedNotice ref="saveNotice" />
        <div class="btn-group btn-sm">
          <button ref="saveButton"
                  class="btn btn-sm btn-group"
                  @click="$refs.saveAsNewNameInput.open()"
          >
            Save as new Template
          </button>
          <button ref="saveButton"
                  class="btn btn-sm btn-primary btn-group"
                  @click="save"
          >
            Save
          </button>
        </div>
        <a class="btn btn-sm btn-link-icon ml-2 tooltip tooltip-left"
           href="/template"
           data-tooltip="Unsaved changes will be discarded!"
        >
          <x-icon size="16" />
        </a>
      </div>
    </div>
    <multi-select-modal
      ref="stylesSelector"
      title="Select Stylesheets"
      :api-fetch="stylesheetApiFetch"
      :default-selection="selectedStylesheets"
      :none="false"
      edit-link="/stylesheets"
      @doku-selection-made="setSelectedStylesheets"
    />
    <text-modal
      ref="saveAsNewNameInput"
      title="Save as new Template"
      @doku-text-entered="saveAsNew"
    />
  </div>
</template>

<script>
import {mapActions, mapState} from 'vuex';
import {XIcon} from 'vue-feather-icons';
import TextModal from '../ui/modal/TextModal';
import MultiSelectModal from '../ui/modal/MultiSelectModal';
import Editor from '../ui/Editor';
import * as actionTypes from '../../store/types/actions';
import AnimatedNotice from '../ui/AnimatedNotice';
import stylesheetApi from '../../api/stylesheet';
import templateApi from '../../api/template';

export default {
  name: 'TemplateEditor',
  components: {
    AnimatedNotice,
    MultiSelectModal,
    TextModal,
    Editor,
    XIcon
  },
  data() {
    return {
      stylesheetApiFetch: stylesheetApi.fetchStylesheets
    };
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
      };
      console.log(data);
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
      });
    },
    updateEditor() {
      this.$refs.editor.editor.refresh();
      this.$refs.editor.editor.focus();
    }
  }
};
</script>

<style scoped>

</style>
