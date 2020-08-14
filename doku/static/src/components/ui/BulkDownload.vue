<template>
  <modal ref="modal" title="Bulk Download">
    <div class="modal-body">
      <div class="content">
        <div class="d-block text-right">
          <button @click="selectAll" class="btn btn-sm">
            All
          </button>
          <button @click="selectNone" class="btn btn-sm">
            None
          </button>
        </div>
        <div>
          <div v-for="document in documents" :key="document.id" class="form-group">
            <label class="form-checkbox c-hand">
              <input type="checkbox" @change="select(document.id, $event)" :checked="selection.has(document.id)" :disabled="loading">
              <i class="form-icon"></i> {{ document.name }}
            </label>
          </div>
        </div>
        <pagination :page="this.page" :pagination="pagination" :callback="setPage"></pagination>
      </div>
    </div>
    <div class="modal-footer">
      <a href="/account/downloads" class="btn btn-link float-left">
        View Download Requests
      </a>
      <animated-notice ref="downloadNotice"></animated-notice>
      <button @click="close" class="btn btn-link">
        Close
      </button>
      <button class="btn btn-primary ml-2" @click="download">
        Download
      </button>
    </div>
  </modal>
</template>

<script>
  import documentApi from '../../api/document';
  import Modal from "./Modal";
  import AnimatedNotice from "./AnimatedNotice";
  import Pagination from './Pagination.vue';

  export default {
    name: 'BulkDownload',
    components: {Modal, Pagination, AnimatedNotice},
    data() {
      return {
        documents: [],
        selection: new Set(),
        allIDs: [],
        pagination: {
          has_next: false,
          has_prev: false,
          pages: []
        },
        page: 1,
        loaded: {},
        allSelected: false,
        noneSelected: false,
        loading: false,
        returnToOldPage: -1
      }
    },
    mounted() {
      this.update();
      documentApi.fetchIDs()
        .then(res => this.allIDs = res.data.result)
        .catch(console.error);
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
          documents: this.documents,
          pagination: this.pagination
        });
        // Change the page
        this.page = p;
        // Fetch or update documents and pagination objects
        this.update();
      },
      selectionChanged() {
        this.allSelected = false;
        this.noneSelected = false;
      },
      select(ID, event) {
        this.selectionChanged();
        if (event.target.checked) {
          this.selection.add(ID);
        } else {
          this.selection.delete(ID);
        }
      },
      fetch(page) {
        return new Promise((resolve, reject) => {
          if (this.loaded.hasOwnProperty(page)) {
            resolve();
            return;
          }
          documentApi.fetchDocuments({params: {page: page}})
            .then(res => {
              this.$set(this.loaded, page, {
                documents: res.data.result,
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
            this.documents = this.loaded[this.page].documents;
            this.pagination = this.loaded[this.page].pagination;
          });
      },
      selectAll(event) {
        event.target.classList.add("loading");
        this.allSelected = true;
        this.noneSelected = false;

        this.selection = new Set(this.allIDs);

        event.target.classList.remove("loading");
      },
      selectNone(event) {
        event.target.classList.add("loading");
        this.allSelected = false;
        this.noneSelected = true;

        this.selection = new Set();

        event.target.classList.remove("loading");
      },
      download(event) {
        event.target.classList.add("loading");
        documentApi.bulkDownload(Array.from(this.selection), [], this.allSelected)
          .then(() => window.location.href = "/account/downloads")
          .catch(err => {
            event.target.classList.remove("loading");
            console.error(err);
            this.$refs.downloadNotice.trigger('Failed!', 'text-error');
          });
      }
    }
  }
</script>

<style scoped>

</style>
