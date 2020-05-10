<template>
  <div class="columns col-gapless doku-edit-cols">
    <div class="column doku-edit-left">
      <Tabs class="tab-block" v-bind:tabs="tabs"></Tabs>
      <variable-editor ref="varEditor" v-show="tabs[0].active" class="tab-content tab-content-vars"></variable-editor>
      <template-editor v-show="tabs[1].active" class="tab-content tab-content-template" ref="templateEditor" v-bind:value="template.source"></template-editor>
      <document-settings v-show="tabs[2].active" class="tab-content tab-content-settings" ref="documentSettings"></document-settings>
    </div>
    <div class="column doku-edit-right">
      <preview v-bind:url="document.render_url"></preview>
    </div>
  </div>
</template>

<script>
  import {mapState, mapActions} from 'vuex';

  import Preview from '../components/pdf/preview.vue';
  import modal from '../components/ui/Modal.vue';
  import StylesModal from '../components/ui/StylesheetModal.vue';
  import Tabs from '../components/ui/Tabs.vue';

  import InlineVariable from '../components/ui/InlineVariable';
  import VariableEditor from '../components/ui/VariableEditor';
  import DocumentSettings from '../components/ui/DocumentSettings';
  import TemplateEditor from '../components/ui/TemplateEditor';

  const TABS = [
    {
      title: 'Document',
      active: false,
    },
    {
      title: 'Template',
      active: false,
    },
    {
      title: 'Settings',
      active: false
    }
  ];

  export default {
    name: 'Edit',
    components: {
      TemplateEditor,
      VariableEditor,
      DocumentSettings,
      Preview,
      Tabs,
    },
    computed: mapState({
      document: state => state.document.document,
      template: state => state.template.template,
      variables: state => state.variable.variables
    }),
    data() {
      return {
        tabs: TABS,
      }
    },
    mounted() {
      if (this._keyListeners !== undefined) {
        document.addEventListener('keydown', this._keyListeners);
      }
    },
    beforeDestroy() {
      if (this._keyListeners !== undefined) {
        document.removeEventListener('keydown', this._keyListeners);
      }
    },
    watch: {
      tabs: {
        immediate: false,
        deep: true,
        handler(newValue, oldValue) {
          if (this.$refs.editor !== undefined || this.$refs.varEditor !== undefined) {
            this.$nextTick(() => {
              if (newValue[0].active) {
                this.$refs.varEditor.updateEditors();
              } else if (newValue[1].active) {
                this.$refs.templateEditor.updateEditor();
              }
            }, 200);
          }
        }
      },
    },
    methods: {
      _keyListeners(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
          e.preventDefault();
          this.save();
        }
      },
      save() {
        if (this.tabs[0].active) {
          this.$refs.varEditor.save(undefined, false);
        } else if (this.tabs[1].active) {
          this.$refs.templateEditor.save();
        }
      }
    }
  }
</script>

<style scoped>
</style>
