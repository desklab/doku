<template>
  <div class="doku-inline-var" draggable="true" @dragstart="startDrag">
    <div class="doku-inline-head" @click.self="showCode =! showCode">
      <code>{{ variable.name }}</code>
      <span v-if="variable.is_list" class="chip">List</span>
      <span v-if="!variable.used" class="chip">Unused</span>
      <div class="dropdown dropdown-right">
        <animated-notice ref="saveNotice" />
        <div class="btn-group btn-sm">
          <button ref="saveButton" class="btn btn-sm btn-primary" @click.self="save">
            Save
          </button>
          <a class="btn btn-sm p-0 dropdown-toggle btn-primary" tabindex="0">
            <more-vertical-icon size="16" />
          </a>
          <ul class="menu">
            <li v-if="!variable.is_list" class="menu-item">
              <button :id="'copy'+String(variable.id)">
                <copy-icon size="14" />
                Copy
              </button>
            </li>
            <li class="menu-item menu-item-error text-error">
              <button @click="remove">
                <trash-icon size="14" />
                Remove
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-show="showCode" class="doku-inline-var-code">
      <div v-if="variable.is_list" class="doku-inline-var-controls">
        <div class="form-inline">
          <input ref="cssClassInput" type="text" placeholder="CSS Class" class="form-input input-sm" :value="variable.css_class">
        </div>
      </div>
      <variable-editor v-if="!variable.is_list && !variable.uses_snippet" ref="editor" :variable="variable" :document-id="documentId">
        <button class="ml-auto mr-2 btn btn-sm" @click="$refs.snippetSelector.open()">
          <scissors-icon size="18" />
          Snippet
        </button>
      </variable-editor>
      <div v-else-if="variable.is_list && !variable.uses_snippet" class="m-2">
        <button class="btn btn-sm mb-2" @click="$refs.addModal.open()">
          <plus-icon size="18" />
          Add
        </button>
        <InlineVariable v-for="childVariable in variable.children" ref="children" :key="childVariable.id" :document-id="documentId" :variable="childVariable" />
        <Modal ref="addModal" class="modal-sm" :title="'Add Child'">
          <div class="modal-body">
            <div class="content">
              <div class="form-group p-2">
                <label class="form-label">Name</label>
                <input ref="childNameInput" name="name" class="form-input" type="text" placeholder="Name" pattern="^.{1,}$" required @keyup="$event.target.classList.remove('is-error')">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <AnimatedNotice ref="addNotice" />
            <button class="btn btn btn-primary" @click="addChild">
              Save
            </button>
            <button class="btn btn-link" @click="$refs.addModal.close()">
              Close
            </button>
          </div>
        </Modal>
      </div>
      <div v-else-if="!variable.is_list && variable.uses_snippet">
        <div class="doku-inline-var-code">
          <div class="doku-inline-var-controls">
            <span>
              <b>Snippet: </b>
              <a class="text-dark" :href="'/snippet/' + String(variable.snippet.id)">{{ variable.snippet.name }}</a>
            </span>
            <button class="btn btn-sm" @click="$refs.snippetSelector.open()">
              <scissors-icon size="18" />
              Snippet
            </button>
          </div>
        </div>
      </div>
    </div>
    <Modal ref="removeModal" class="modal-sm" :title="'Delete Variable'">
      <div class="modal-body">
        <div class="content">
          Do you really want to remove <code>{{ variable.name }}</code>
        </div>
      </div>
      <div class="modal-footer">
        <AnimatedNotice ref="removeNotice" />
        <button class="btn btn btn-error" @click="remove($event, true)">
          Delete
        </button>
        <button class="btn btn-link" @click="$refs.removeModal.close()">
          Close
        </button>
      </div>
    </Modal>
    <select-modal ref="snippetSelector" title="Select Snippet" :api-fetch="snippetApiFetch" :default-selection="variable.snippet" :none="true" @doku-selection-made="setSelectedSnippet" />
  </div>
</template>

<script>
import ClipboardJS from 'clipboard';
import {mapActions} from 'vuex';
import {
  MoreVerticalIcon,
  CopyIcon,
  PlusIcon,
  TrashIcon,
  ScissorsIcon
} from 'vue-feather-icons';

import Editor from '../ui/Editor.vue';
import Modal from '../ui/modal/Modal';
import AnimatedNotice from '../ui/AnimatedNotice';
import * as actionTypes from '../../store/types/actions';
import AnimatedToggle from '../ui/form/AnimatedToggle';
import VariableEditor from './VariableEditor';
import SelectModal from '../ui/modal/SelectModal';
import snippetApi from '../../api/snippet';

export default {
  name: 'InlineVariable',
  components: {
    SelectModal,
    VariableEditor,
    AnimatedToggle,
    AnimatedNotice,
    Modal,
    Editor,
    CopyIcon, MoreVerticalIcon, PlusIcon, TrashIcon, ScissorsIcon
  },
  props: {
    variable: {
      type: Object
    },
    documentId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      showCode: false,
      _showDone: false,
      snippetApiFetch: snippetApi.fetchSnippets
    };
  },
  watch: {
    showCode: function (newValue, oldValue) {
      if (newValue) {
        if (!this.variable.is_list && !this.variable.uses_snippet) {
          this.$nextTick(() => {
            this.$refs.editor.refresh();
          });
        }
      }
    }
  },
  mounted() {
    new ClipboardJS('#copy' + String(this.variable.id), {
      text: () => this.$refs.editor.getValue()
    });
  },
  methods: {
    ...mapActions('variable', [
      actionTypes.REMOVE_VARIABLE,
      actionTypes.UPDATE_VARIABLES,
      actionTypes.CREATE_VARIABLE
    ]),
    startDrag(event) {
      event.dataTransfer.dropEffect = 'move';
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('variableId', this.variable.id);
    },
    save(event) {
      event.target.classList.add('loading');
      let data = this.getData();
      this.updateVariables(data)
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
    remove(event, sure) {
      if (!sure) {
        this.$refs.removeModal.open();
        return;
      }
      event.target.classList.add('loading');
      this.removeVariable(this.variable.id)
        .then(() => {
          if (this.$refs.removeModal !== undefined) {
            // As this element is probably going to be removed, closing the
            // modal is redundant. Also, $refs will no longer be available.
            this.$refs.removeModal.close();
          }
        })
        .catch((err) => {
          console.error(err);
          this.$refs.removeNotice.trigger('Failed!', 'text-error');
        })
        .finally(() => {
          event.target.classList.remove('loading');
        });
    },
    getData() {
      // Define default data object
      let _data = {
        id: this.variable.id,
        document_id: this.documentId,
      };

      if (this.variable.is_list) {
        // This document is a list. Thus, the children property
        // (which is a list) has to be populated. This is done by
        // iterating over all children and requesting their data
        // recursively.
        _data.children = [];
        _data.content = '';
        _data.css_class = this.$refs.cssClassInput.value;
        if (this.$refs.children !== undefined ) {
          // Note: If only one children is present, the children ref is
          // not an array. This case must be
          if (Array.isArray(this.$refs.children)) {
            _data.children.push(
              ...this.$refs.children.map(c => c.getData())
            );
          } else {
            _data.children.push(this.$refs.children.getData());
          }
        }
      } else if (!this.variable.uses_snippet) {
        _data.use_markdown = this.$refs.editor.getUseMarkdown();
        _data.content = this.$refs.editor.getValue();
        _data.css_class = this.$refs.editor.getCssClass();
      }
      return _data;
    },
    setSelectedSnippet(snippet) {
      let data = {
        id: this.variable.id,
        snippet_id: (snippet === null || snippet === undefined) ? null : snippet.id
      };
      this.updateVariables(data)
        .then(() => {
          this.$refs.saveNotice.trigger('Success!', 'text-dark');
        })
        .catch((err) => {
          console.error(err);
          this.$refs.saveNotice.trigger('Failed!', 'text-error');
        });
    },
    addChild(event) {
      let existingNames = this.variable.children.map(c => c.name);
      if (
        !this.$refs.childNameInput.checkValidity()
          || existingNames.includes(this.$refs.childNameInput.value)
      ) {
        this.$refs.childNameInput.classList.add('is-error');
        return;
      }
      let data = {
        name: this.$refs.childNameInput.value,
        parent_id: this.variable.id,
        document_id: this.documentId
      };
      event.target.classList.add('loading');
      this.createVariable(data)
        .then(() => {
          this.$nextTick(() => {
            if (this.$refs.addModal !== undefined) {
              this.$refs.addModal.close();
            }
          });
        })
        .catch((err) => {
          console.error(err);
          this.$refs.addNotice.trigger('Failed!', 'text-error');
        })
        .finally(() => {
          event.target.classList.remove('loading');
        });
    },
    updateEditor() {
      if (this.showCode) {
        this.$refs.editor.refresh();
      }
    },
  }
};
</script>

<style scoped>

</style>
