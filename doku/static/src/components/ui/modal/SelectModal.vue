<template>
  <modal ref="modal" :title="title">
    <div class="modal-body">
      <div class="content">
        <div v-for="item in items" :key="item.id" class="form-group">
          <label class="form-radio c-hand">
            <input type="radio" name="item" :value="item.id" @change="select(item.id, $event)" :checked="selectedItem === item.id">
            <i class="form-icon"></i> {{ item.name }}
          </label>
        </div>
        <pagination :page="this.page" :pagination="pagination" :callback="setPage"></pagination>
      </div>
    </div>
    <div class="modal-footer">
      <button v-if="none" class="btn btn-link float-left" @click="selectNone()">
        Select None
      </button>
      <button @click="close" class="btn btn-link">
        Close
      </button>
      <button class="btn btn-primary ml-2" @click="saveSelection()">
        Select
      </button>
    </div>
  </modal>
</template>

<script>
import Modal from "./Modal";
import Pagination from "../Pagination";
import AnimatedNotice from "../AnimatedNotice";

/**
 * Select Modal
 *
 * Modal used to select items (e.g. a template). This is used to
 * replace the simple `<select>` HTML element which does not support
 * pagination.
 * The items must be a list of objects containing an id.
 *
 * @param {Function} apiFetch - An API function that can be called
 *   to get all items (with pagination).
 * @param {String} title - Passed to the modal component.
 * @param {Number} defaultSelection - The default selection (current
 *   selection).
 * @param {Boolean} none - Add option for selecting no item using a
 *   button (Select None).
 *
 * @event doku-selection-made: Passes the selected item when the modal
 *   is closed and a selection has been made.
 */

export default {
  name: 'SelectModal',
  components: {
    Modal,
    Pagination,
    AnimatedNotice
  },
  props: {
    apiFetch: Function,
    title: String,
    defaultSelection: Number,
    none: Boolean
  },
  data() {
    return {
      items: [],
      selectedItem: null,
      pagination: {
        has_next: false,
        has_prev: false,
        pages: []
      },
      page: 1,
      loaded: {}
    }
  },
  mounted() {
    this.selectedItem = this.defaultSelection;
  },
  methods: {
    toggle() {
      this.$refs.modal.toggle();
    },
    open() {
      this.selectedItem = this.defaultSelection;
      this.update();
      this.$refs.modal.open();
    },
    close() {
      this.$refs.modal.close();
    },
    setPage(p) {
      // Update the current page
      this.$set(this.loaded, this.page, {
        items: this.items,
        pagination: this.pagination
      });
      // Change the page
      this.page = p;
      // Fetch or update items and pagination objects
      this.update();
    },
    select(id, event) {
      if (event.target.checked) {
        this.selectedItem = id;
      }
    },
    fetch(page) {
      return new Promise((resolve, reject) => {
        if (this.loaded.hasOwnProperty(page)) {
          resolve();
          return;
        }
        this.apiFetch({params: {page: page}})
          .then(res => {
            this.$set(this.loaded, page, {
              items: res.data.result,
              pagination: res.data.meta
            });
            resolve();
          })
          .catch(reject);
      });
    },
    update() {
      this.fetch(this.page)
        .then(() => {
          this.items = this.loaded[this.page].items;
          this.pagination = this.loaded[this.page].pagination;
        });
    },
    saveSelection() {
      this.close();
      this.$emit('doku-selection-made', this.selectedItem);
    },
    selectNone() {
      this.selectedItem = null;
      this.saveSelection();
    }
  }
}
</script>

<style scoped>

</style>
