<template>
  <modal ref="modal" title="Select Snippet">
    <div class="modal-body">
      <div class="content">
        <div v-for="snippet in snippets" :key="snippet.id" class="form-group">
          <label class="form-radio c-hand">
            <input type="radio" name="snippet" :value="snippet.id" @change="select(snippet.id, $event)" :checked="selectedSnippet === snippet.id" :disabled="loading">
            <i class="form-icon"></i> {{ snippet.name }}
          </label>
        </div>
        <pagination :page="this.page" :pagination="pagination" :callback="setPage"></pagination>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-link float-left" @click="selectNone()">
        Select None
      </button>
      <button @click="close" class="btn btn-link">
        Close
      </button>
      <button class="btn btn-primary ml-2" @click="save()">
        Save
      </button>
    </div>
  </modal>
</template>

<script>
import snippetApi from '../../api/snippet';
import Modal from "../ui/Modal";
import AnimatedNotice from "../ui/AnimatedNotice";
import Pagination from '../ui/Pagination.vue';

export default {
  name: 'SelectSnippet',
  components: {Modal, Pagination, AnimatedNotice},
  props: {
    callback: Function
  },
  data() {
    return {
      snippets: [],
      selectedSnippet: null,
      pagination: {
        has_next: false,
        has_prev: false,
        pages: []
      },
      page: 1,
      loaded: {},
      loading: false,
      returnToOldPage: -1
    }
  },
  mounted() {
    this.update();
  },
  methods: {
    toggle() {
      this.$refs.modal.toggle();
    },
    open() {
      this.$refs.modal.open();
    },
    close() {
      this.$refs.modal.close();
    },
    setPage(p) {
      // Update the current page
      this.$set(this.loaded, this.page, {
        snippets: this.snippets,
        pagination: this.pagination
      });
      // Change the page
      this.page = p;
      // Fetch or update snippets and pagination objects
      this.update();
    },
    selectionChanged() {
      this.allSelected = false;
      this.noneSelected = false;
    },
    select(ID, event) {
      this.selectionChanged();
      if (event.target.checked) {
        this.selectedSnippet = ID;
      }
    },
    fetch(page) {
      return new Promise((resolve, reject) => {
        if (this.loaded.hasOwnProperty(page)) {
          resolve();
          return;
        }
        snippetApi.fetchSnippets({params: {page: page}})
          .then(res => {
            this.$set(this.loaded, page, {
              snippets: res.data.result,
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
          this.snippets = this.loaded[this.page].snippets;
          this.pagination = this.loaded[this.page].pagination;
        });
    },
    save() {
      this.close();
      this.callback(this.selectedSnippet);
    },
    selectNone() {
      this.selectedSnippet = null;
      this.save();
    }
  }
}
</script>

<style scoped>

</style>
