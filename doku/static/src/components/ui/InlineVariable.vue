<template>
  <div class="doku-inline-var">
    <div v-on:click.self="showCode =! showCode" class="doku-inline-head">
      <code>{{ variable.name }}</code>
      <span v-if="variable.is_list" class="chip">
        List
      </span>
      <span v-if="!variable.used" class="chip">
        Unused
      </span>
      <div class="dropdown dropdown-right">
        <transition name="fade-out">
          <span v-if="$data._showDone" class="text-dark mr-2">Done!</span>
        </transition>
        <div class="btn-group btn-sm">
          <button @click.self="save" ref="saveButton" class="btn btn-sm btn-primary">Save</button>
          <a class="btn btn-sm p-0 dropdown-toggle btn-primary" tabindex="0">
            <more-vertical-icon size="16"></more-vertical-icon>
          </a>
          <ul class="menu">
            <li v-if="!variable.is_list" class="menu-item">
              <a href="#" id="copy">
                <copy-icon size="14"></copy-icon>
                Copy
              </a>
            </li>
            <li class="menu-item menu-item-error text-error">
              <button @click="remove">
                <trash-icon size="14"></trash-icon>
                Remove
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-show="showCode">
      <Editor v-if="!variable.is_list" ref="editor" v-bind:mode="'text/x-markdown'" v-bind:value="variable.content" v-bind:height="'auto'"></Editor>
      <div class="m-2" v-else>
        <button @click="$refs.addModal.open()" class="btn btn-sm mb-2">
          <plus-icon size="18"></plus-icon>
          Add
        </button>
        <InlineVariable v-for="childVariable in variable.children" :key="childVariable.name" :variable="childVariable"></InlineVariable>
        <Modal class="modal-sm" ref="addModal" v-bind:title="'Add Child'">
          <div class="modal-body">
            <div class="content">
              <div class="form-group p-2">
                <label class="form-label" for="childNameInput">Name</label>
                <input v-on:keyup="$event.target.classList.remove('is-error')" name="name" class="form-input" type="text" id="childNameInput" placeholder="Name" pattern="^.{1,}$" required>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="addChild" class="btn btn btn-primary">
              Save
            </button>
            <button @click="$refs.addModal.close()" class="btn btn-link">
              Close
            </button>
          </div>
        </Modal>
      </div>
    </div>
    <Modal class="modal-sm" ref="deleteModal" v-bind:title="'Delete Variable'">
      <div class="modal-body">
        <div class="content">
          Do you really want to delete <code>{{ variable.name }}</code>
        </div>
      </div>
      <div class="modal-footer">
        <button @click="remove" class="btn btn btn-error">
          Delete
        </button>
        <button @click="$refs.deleteModal.close()" class="btn btn-link">
          Close
        </button>
      </div>
    </Modal>
  </div>
</template>

<script>
  import ClipboardJS from 'clipboard';
  import axios from "axios";
  import { MoreVerticalIcon, CopyIcon, PlusIcon, TrashIcon } from 'vue-feather-icons';

  import Editor from './Editor.vue';
  import Modal from "./Modal";


  axios.defaults.xsrfCookieName = 'csrf_token';
  axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';

  export default {
    name: 'InlineVariable',
    props: {
      variable: {
        type: Object
      },
      documentId: {
        type: Number,
        default: null
      }
    },
    components: {
      Modal,
      Editor
      Editor,
      CopyIcon, MoreVerticalIcon, PlusIcon, TrashIcon
    },
    data() {
      return {
        showCode: false,
        _showDone: false
      }
    },
    mounted() {
      new ClipboardJS('#copy', {
        text: () => this.$refs.editor.getValue()
      });
    },
    watch: {
      showCode: function (newValue, oldValue) {
        if (newValue) {
          if (!this.variable.is_list) {
            setTimeout(() => {
              this.$refs.editor.editor.refresh();
              this.$refs.editor.editor.focus();
            }, 100);
          }
        }
      }
    },
    methods: {
      save(event) {
        event.target.classList.add('loading');
        let data = {
          content: this.$refs.editor.getValue()
        };
        let url = this.variable.api_url;
        axios
          .post(url, data)
          .then((response) => {
            this._animateShowDone();
            this.variable = response.data;
          })
          .catch((error) => {
            console.error(error);
          })
          .finally(() => {
            event.target.classList.remove('loading');
          });
      },
      remove(event) {
        event.target.classList.add('loading');
        axios.delete(this.variable.delete_url)
          .then((response) => {
            this.$refs.deleteModal.close();
          })
          .finally(() => {
            event.target.classList.remove('loading');
          });
      },
      refreshEditor() {
        if (this.showCode) {
          this.$refs.editor.editor.refresh();
        }
      },
      _animateShowDone() {
        this.$data._showDone = true;
        setTimeout(() => {
          this.$data._showDone = false
        }, 2000);
      },
      getData() {
        return {
          id: this.variable.id,
          content: !this.variable.is_list ? this.$refs.editor.getValue() : ''
        }
      },
      addChild(event) {
        let childNameInput = document.getElementById('childNameInput');
        let existingNames = this.variable.children.map(c => c.name);
        if (
          !childNameInput.checkValidity()
          || existingNames.includes(childNameInput.value)
        ) {
          childNameInput.classList.add('is-error');
          return;
        }
        event.target.classList.add('loading');
        axios
          .post(this.variable.create_url, {
            name: childNameInput.value,
            parent_id: this.variable.id,
            document_id: this.documentId,
          })
          .then(function (response) {
            this.variable.children.push(response.data);
          })
          .catch(function (error) {
            console.error(error);
          })
          .finally(function () {
            event.target.classList.remove('loading');
          });
      }
    }
  }
</script>

<style scoped>

</style>
