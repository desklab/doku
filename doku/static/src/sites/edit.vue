<template>
  <div class="columns col-gapless doku-edit-cols">
    <div class="column doku-edit-left">
      <Tabs class="tab-block" v-bind:tabs="tabs"></Tabs>
      <multi-variable-editor ref="varEditor" v-show="tabs[0].active" class="tab-content tab-content-vars"></multi-variable-editor>
      <document-settings v-show="tabs[1].active" class="tab-content tab-content-settings" ref="documentSettings"></document-settings>
    </div>
    <div class="column doku-edit-right">
      <preview v-bind:url="document.render_url"></preview>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex';

  import Preview from '../components/pdf/preview.vue';
  import Tabs from '../components/ui/Tabs.vue';

  import MultiVariableEditor from '../components/document/MultiVariableEditor';
  import DocumentSettings from '../components/document/DocumentSettings';
  import TemplateEditor from '../components/template/TemplateEditor';

  const TABS = [
    {
      title: 'Document',
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
      MultiVariableEditor,
      DocumentSettings,
      Preview,
      Tabs,
    },
    computed: mapState({
      document: state => state.document.document,
      template: state => state.template.template,
    }),
    data() {
      return {
        tabs: TABS,
      }
    },
    mounted() {
      if (this._keyListeners !== undefined) {
        window.document.addEventListener('keydown', this._keyListeners);
      }
    },
    beforeDestroy() {
      if (this._keyListeners !== undefined) {
        window.document.removeEventListener('keydown', this._keyListeners);
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
