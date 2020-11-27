<template>
  <div class="border rounded p-4 bg-gray">
    <text-edit :text="stylesheet.name" :save="saveName" :placeholder="'Name'" />
    <span v-if="isEmpty" class="chip bg-error">Empty</span>
    <span v-if="!isUsed" class="chip bg-warning">Unused</span>
    <span v-if="numberOfUses > 1" class="chip text-success">
      Used by {{ numberOfUses }} templates
    </span>
    <span v-if="numberOfUses === 1" class="chip text-success">
      Used by {{ numberOfUses }} template
    </span>
    <div class="btn-group btn-sm float-right">
      <animated-notice ref="notice" />
      <button class="btn btn-primary btn-sm btn-group" @click="$refs.editModal.show()">
        Edit
      </button>
      <button class="btn btn-sm btn-black-outline btn-group" @click="deleteStyle">
        <trash2-icon size="16"></trash2-icon>
      </button>
    </div>
    <modal title="Update Stylesheet" ref="editModal" class="modal-sm">
      <div class="modal-body">
        <input ref="sourceFile"
               accept="text/css"
               name="source"
               type="file"
               @change="check_input"
        >
      </div>
      <div class="modal-footer">
        <button :disabled="isEmpty"
                class="btn btn-link float-left"
                @click="clearStyleSource"
        >
          Clear
        </button>
        <button ref="updateButton" class="btn float-right" disabled @click="upload">
          Update
        </button>
      </div>
    </modal>
  </div>
</template>

<script>
import {mapActions} from 'vuex';
import {Trash2Icon} from 'vue-feather-icons';
import * as actionTypes from '../../store/types/actions';
import AnimatedNotice from '../ui/AnimatedNotice';
import TextEdit from '../ui/form/TextEdit';
import Modal from '../ui/modal/Modal';


export default {
  name: 'StyleItem',
  components: {
    TextEdit, Trash2Icon,
    AnimatedNotice, Modal
  },
  props: {
    stylesheet: {
      type: Object,
      default: undefined
    }
  },
  computed: {
    isEmpty: function() {
      return this.stylesheet.source == null;
    },
    isUsed: function() {
      return this.numberOfUses > 0;
    },
    numberOfUses: function() {
      if (this.stylesheet.templates !== undefined)
        return this.stylesheet.templates.length;
      else
        return 0;
    }
  },
  methods: {
    ...mapActions('stylesheet', [
      actionTypes.UPLOAD_STYLESHEET,
      actionTypes.UPDATE_STYLESHEET,
      actionTypes.DELETE_STYLESHEET
    ]),
    ...mapActions('template', [
      actionTypes.REMOVE_STYLESHEET_FROM_TEMPLATE
    ]),
    upload(event) {
      event.target.classList.add('loading');
      let formData = new FormData();
      formData.append('source', this.$refs.sourceFile.files[0]);
      this.uploadStylesheet({
        url: this.stylesheet.upload_url,
        formData: formData
      })
        .then(() => {
          this.$refs.notice.trigger('Success!', 'text-dark');
        })
        .catch(err => {
          console.error(err);
          this.$refs.notice.trigger('Failed!', 'text-error');
        })
        .finally(() => {
          event.target.classList.remove('loading');
        });
      this.$refs.sourceFile.value = null;
      this.$refs.updateButton.disabled = true;
    },
    deleteStyle(event) {
      event.target.classList.add('loading');
      let data = {
        url: this.stylesheet.delete_url,
        id: this.stylesheet.id
      };
      this.deleteStylesheet(data)
        .then(() => {
          // This element should be removed anyway
        })
        .catch(err => {
          console.error(err);
          this.$refs.notice.trigger('Failed!', 'text-error');
        })
        .finally(() => {
          event.target.classList.remove('loading');
        });
    },
    clearStyleSource() {
      let data = {
        id: this.stylesheet.id,
        source: null
      };
      this.updateStylesheet(data)
        .then(() => {
          this.$refs.notice.trigger('Success!', 'text-dark');
        })
        .catch(err => {
          console.error(err);
          this.$refs.notice.trigger('Failed!', 'text-error');
        });
    },
    saveName(name) {
      let data = {
        id: this.stylesheet.id,
        name: name
      };
      this.updateStylesheet(data)
        .then(() => {
          this.$refs.notice.trigger('Success!', 'text-dark');
        })
        .catch(err => {
          console.error(err);
          this.$refs.notice.trigger('Failed!', 'text-error');
        });
    },
    check_input() {
      this.$refs.updateButton.disabled = this.$refs.sourceFile.files.length === 0;
    }
  },
};
</script>

<style scoped>

</style>
