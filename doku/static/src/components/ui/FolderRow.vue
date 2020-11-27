<template>
  <div>
    <div
      ref="folderRow"
      class="folder-row c-hand"
      @click.self="toggle"
      @drop="onDrop($event, 'root')"
      @dragover.prevent="onDragOver"
      @dragleave="onDragLeave"
      @dragenter.prevent
    >
      <img
        v-if="!displayFolderOpen && hasImage"
        class="m-3"
        :src="defaultImage"
        alt="Folder"
      >
      <img
        v-else-if="displayFolderOpen && hasImage"
        class="m-3"
        :src="hoverImage"
        alt="Folder"
      >
      <text-edit
        :class="hasImage ? '' : 'm-4'" :text="name"
        placeholder="Name"
        :save="rename"
      />
      <div class="ml-auto">
        <div v-if="createMode && allowAdd" class="input-group input-inline">
          <input
            v-model="newName"
            type="text"
            class="form-input input-sm"
            placeholder="Name"
          >
          <button
            class="btn btn-primary btn-sm input-group-btn"
            :disabled="newName.replaceAll(' ','').length < 1"
            @click="createNew"
          >
            <check-icon size="16" />
          </button>
          <button class="btn btn-sm input-group-btn" @click="hideCreateNew">
            <x-icon size="16" />
          </button>
        </div>
        <button v-if="allowAdd" class="btn btn-link-icon mr-2" @click="showCreateNew">
          <folder-plus-icon size="24" />
        </button>
        <button
          v-if="allowRemove"
          class="btn btn-link-icon mr-2"
          @click="$emit('doku-remove-folder', $event)"
        >
          <trash2-icon size="24" />
        </button>
      </div>
    </div>
    <div
      v-show="isOpen"
      ref="itemList"
      class="folder-content"
      @drop="onDrop($event, 'list')"
      @dragover.prevent="onDragOverList"
      @dragleave="onDragLeave"
      @dragenter.prevent
    >
      <slot />
    </div>
  </div>
</template>

<script>
import { Trash2Icon, FolderPlusIcon, CheckIcon, XIcon } from 'vue-feather-icons';
import TextEdit from './form/TextEdit';


/**
 * Folder Row
 *
 * @event doku-add-folder - Add button has been clicked
 * @event doku-remove-folder - Remove button has been clicked
 * @event doku-rename-folder - Folder has been renamed
 * @event doku-dragend - Custom drag-end for both drop areas
 *
 * @param {String} name - Name of the folder
 * @param {String} defaultImage - Path to the default image
 * @param {String} hoverImage - Path to the hover image
 * @param {Boolean} hasImage - Show folder image
 * @param {Boolean} nested - Nested folder: Prevent dragover on list
 * @param {Boolean} alwaysOpen - Folder is not closeable
 * @param {Boolean} allowRemove - Show remove button + add event
 * @param {Boolean} allowAdd - Show add button + add event
 */
export default {
  name: 'FolderRow',
  components: {
    TextEdit,
    Trash2Icon,
    FolderPlusIcon,
    CheckIcon,
    XIcon
  },
  props: {
    name: {
      type: String,
      default: ''
    },
    defaultImage: {
      type: String,
      default: '/static/assets/folder.svg'
    },
    hoverImage: {
      type: String,
      default: '/static/assets/folder_open.svg'
    },
    hasImage: {
      type: Boolean,
      default: true
    },
    nested: {
      type: Boolean,
      default: false
    },
    alwaysOpen: {
      type: Boolean,
      default: false
    },
    allowRemove: {
      type: Boolean,
      default: false
    },
    allowAdd: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isOpen: this.alwaysOpen,
      displayFolderOpen: this.alwaysOpen,
      createMode: false,
      newName: '',
    };
  },
  methods: {
    onDragOver() {
      this.$refs.folderRow.classList.add('doku-dragover');
      this.displayFolderOpen = true;
    },
    onDragLeave() {
      this.$refs.folderRow.classList.remove('doku-dragover');
      this.$refs.itemList.classList.remove('doku-dragover');
      this.displayFolderOpen = this.isOpen;
    },
    onDragOverList() {
      if (!this.nested) {
        this.$refs.itemList.classList.add('doku-dragover');
      }
    },
    onDrop(event, origin) {
      this.onDragLeave();
      if (origin === 'list' && this.nested) {
        return;
      } else {
        event.preventDefault();
        this.$emit('doku-dragend', event);
      }
    },
    toggle() {
      if (this.alwaysOpen) {
        // Just do nothing
        return;
      }
      this.isOpen = !this.isOpen;
      this.displayFolderOpen = this.isOpen;
    },
    showCreateNew() {
      this.createMode = true;
    },
    hideCreateNew() {
      this.createMode = false;
      // Reset field after closing
      this.newName = '';
    },
    createNew(event) {
      this.createMode = false;
      this.$emit('doku-add-folder', event, this.newName);
      this.newName = '';
    },
    rename(newName) {
      this.$emit('doku-rename-folder', newName);
    }
  }
};
</script>

<style scoped>

</style>
