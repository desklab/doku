<template>
  <div>
    <div ref="folderRow" @click="toggle" class="folder-row c-hand">
      <img v-if="!displayFolderOpen" class="m-3" :src="defaultImage" alt="Folder">
      <img v-else class="m-3" :src="hoverImage" alt="Folder">
      <span>{{ name }}</span>
    </div>
    <div v-show="isOpen" ref="itemList" class="folder-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>

/**
 * Folder Row
 *
 * @param {String} name - Name of the folder
 * @param {String} defaultImage - Path to the default image
 * @param {String} hoverImage - Path to the hover image
 */
export default {
  name: 'FolderRow',
  props: {
    name: String,
    defaultImage: {
      type: String,
      default: '/static/assets/folder.svg'
    },
    hoverImage: {
      type: String,
      default: '/static/assets/folder_open.svg'
    }
  },
  data() {
    return {
      isOpen: false,
      displayFolderOpen: false
    }
  },
  mounted() {
    this.$refs.folderRow.addEventListener('dragover', this.onDragOver);
    this.$refs.folderRow.addEventListener('dragleave', this.onDragLeave);
    this.$refs.itemList.addEventListener('dragover', this.onDragOverList);
    this.$refs.itemList.addEventListener('dragleave', this.onDragLeaveList);
  },
  methods: {
    onDragOver() {
      this.$refs.folderRow.classList.add('doku-dragover');
      this.displayFolderOpen = true;
    },
    onDragLeave() {
      this.$refs.folderRow.classList.remove('doku-dragover');
      this.displayFolderOpen = false;
    },
    onDragOverList() {
      this.$refs.itemList.classList.add('doku-dragover');
    },
    onDragLeaveList() {
      this.$refs.itemList.classList.remove('doku-dragover');
    },
    toggle() {
      this.isOpen = !this.isOpen;
      this.displayFolderOpen = this.isOpen;
    }
  }
}
</script>

<style scoped>

</style>
