<template>
  <div class="columns col-gapless doku-edit-cols">
    <div class="column doku-edit-left">
      <Tabs class="tab-block" :tabs="tabs" />
      <multi-variable-editor
        v-if="tabs[0].active"
        ref="varEditor"
        class="tab-content tab-content-vars"
      />
      <document-settings
        v-if="tabs[1].active"
        ref="documentSettings"
        class="tab-content tab-content-settings"
      />
    </div>
    <div class="column doku-edit-right">
      <preview :url="document.render_url" />
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';

import Preview from '../components/pdf/preview.vue';
import Tabs from '../components/ui/Tabs.vue';

import MultiVariableEditor from '../components/document/MultiVariableEditor';
import DocumentSettings from '../components/document/DocumentSettings';

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
    };
  },
  watch: {
    tabs: {
      immediate: false,
      deep: true,
      handler(newValue) {
        if (this.$refs.editor !== undefined || this.$refs.varEditor !== undefined) {
          this.$nextTick(() => {
            if (newValue[0].active) {
              this.$refs.varEditor.updateEditors();
            }
          }, 200);
        }
      }
    },
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
};
</script>

<style scoped>
</style>
