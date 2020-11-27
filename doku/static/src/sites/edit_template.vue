<template>
  <div class="columns col-gapless doku-edit-cols">
    <div class="column doku-edit-left">
      <TemplateEditor
        ref="templateEditor"
        class="tab-content tab-content-template"
        :value="template.source"
      />
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';

import TemplateEditor from '../components/template/TemplateEditor';

export default {
  name: 'EditTemplate',
  components: {
    TemplateEditor
  },
  computed: mapState({
    template: state => state.template.template,
  }),
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
  methods: {
    _keyListeners(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        this.save();
      }
    },
    save() {
      this.$refs.templateEditor.save();
    }
  }
};
</script>

<style scoped>
</style>
