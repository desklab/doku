<template>
  <div class="columns col-gapless doku-edit-cols">
    <div class="column doku-edit-left">
      <Tabs :class="'tab-block'" v-bind:tabs="tabs"></Tabs>
      <div v-show="tabs[0].active" class="tab-content tab-content-vars">
        <div class="doku-edit-vars">
          <InlineVariable ref="inlineVars" v-for="variable in doc.variables.filter(v => v.parent == null)" :document-id="doc.id" :variable="variable"></InlineVariable>
        </div>
      </div>
      <div v-show="tabs[1].active" class="tab-content tab-content-template">
        <Editor ref="editor" v-bind:value="doc.template.source"></Editor>
      </div>
      <div class="editor-toolbar">
        <button v-show="tabs[1].active" @click="$refs.stylesModal.open()" class="btn btn-sm">Styles</button>
        <span v-show="tabs[0].active"></span>
        <div>
          <transition name="fade-out">
            <span v-if="$data._showDone" class="text-dark mr-2">Done!</span>
          </transition>
          <button ref="saveButton" @click="save(!tabs[0].active)" class="btn btn-primary">
            {{ (tabs[0].active) ? 'Save all' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
    <div class="column doku-edit-right">
      <Preview></Preview>
    </div>
    <modal ref="confirmModal" class="modal-sm" v-bind:title="'Save All'">
      <div class="modal-body">
        <div class="content">
          Do you really want to save all variables
        </div>
      </div>
      <div class="modal-footer">
        <button @click="save(true)" class="btn btn btn-primary">
          Save
        </button>
        <button @click="closeConfirmModal" class="btn btn-link">
          Close
        </button>
      </div>
    </modal>
    <StylesModal v-bind:stylesheets="doc.template.styles" v-bind:base-style="doc.template.base_style" ref="stylesModal"></StylesModal>
  </div>
</template>

<script>
  import axios from "axios";

  import Preview from '../components/pdf/preview.vue';
  import modal from '../components/ui/Modal.vue';
  import StylesModal from '../components/ui/StylesheetModal.vue';
  import Tabs from '../components/ui/Tabs.vue';
  import Editor from '../components/ui/Editor';
  import InlineVariable from '../components/ui/InlineVariable';


  axios.defaults.xsrfCookieName = 'csrf_token';
  axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';

  const TABS = [
    {
      title: 'Document',
      active: false,
    },
    {
      title: 'Template',
      active: false,
    }
  ];

  export default {
    name: 'edit',
    components: {
      Editor, Preview, Tabs, InlineVariable, modal, StylesModal
    },
    data() {
      return {
        tabs: TABS,
        _showDone: false,
        _showPopover: false,
        doc: JSON.parse(window.documentObj)
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
            setTimeout(() => {
              if (newValue[0].active) {
                if (Array.isArray(this.$refs.inlineVars)) {
                  for (let editor in this.$refs.inlineVars) {
                    this.$refs.inlineVars[editor].refreshEditor();
                  }
                } else {
                  this.$refs.inlineVars.refreshEditor();
                }
              } else if (newValue[1].active) {
                this.$refs.editor.editor.refresh();
                this.$refs.editor.editor.focus();
              }
            }, 200);
          }
        }
      },
    },
    methods: {
      save(sure) {
        if (!sure && this.tabs[0].active) {
          this.openConfirmModal();
          return
        }
        this.closeConfirmModal();
        this.$refs.saveButton.classList.add('loading');
        let url = '';
        let data = {};
        if (this.tabs[1].active) {
          url = this.doc.template.update_url;
          data.source = this.$refs.editor.getValue();
        } else if (this.tabs[0].active) {
          url = this.doc.update_url;
          data.variables = [];
          if (Array.isArray(this.$refs.inlineVars)) {
            for (let editor in this.$refs.inlineVars) {
              data.variables.push(this.$refs.inlineVars[editor].getData());
            }
          } else {
            data.variables.push(this.$refs.inlineVars.getData());
          }
        }
        axios
          .put(url, data)
          .then((response) => {
            this._animateShowDone();
            this.doc.template = response.data;
          })
          .catch((error) => {
            console.error(error);
          })
          .finally(() => {
            this.$refs.saveButton.classList.remove('loading');
          });
      },
      closeConfirmModal() {
        this.$refs.confirmModal.close();
      },
      openConfirmModal() {
        this.$refs.confirmModal.open();
      },
      _keyListeners(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
          e.preventDefault();
          this.save();
        }
      },
      _animateShowDone() {
        this.$data._showDone = true;
        setTimeout(() => {
          this.$data._showDone = false
        }, 2000);
      },
    }
  }
</script>

<style scoped>
</style>
