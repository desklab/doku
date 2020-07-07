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
              <input type="checkbox" @change="selectionChanged" v-model="document.checked" :disabled="loading">
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
      <button @click="close" class="btn btn-link">
        Close
      </button>
      <button class="btn btn-primary ml-2">
        Download
      </button>
    </div>
  </modal>
</template>

<script>
  import documentApi from '../../api/document';
  import Modal from "./Modal";
  import Pagination from './Pagination.vue';

  export default {
    name: 'BulkDownload',
    components: {Modal, Pagination},
    data() {
      return {
        documents: [],
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
      fetch(page) {
        return new Promise((resolve, reject) => {
          if (this.loaded.hasOwnProperty(page)) {
            resolve();
            return;
          }
          documentApi.fetchDocuments({ params: {page: page} })
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
        for (let i = 1; i <= this.pagination.page_count; i++) {
          this.fetch(i)
            .then(() => {
              this.updateSelection(i);
            });
        }
        event.target.classList.remove("loading");
      },
      selectNone() {
        event.target.classList.add("loading");
        this.allSelected = false;
        this.noneSelected = true;
        for (let i = 1; i <= this.pagination.page_count; i++) {
          this.fetch(i)
            .then(() => {
              this.updateSelection(i);
            });
        }
        event.target.classList.remove("loading");
      },
      updateSelection(page) {
        if (this.allSelected) {
          if (this.page === page) {
            for (let i in this.documents) {
              this.$set(this.documents[i], "checked", true);
            }
          }
          for (let i in this.loaded) {
            for (let j in this.loaded[i].documents) {
              this.$set(this.loaded[i].documents[j], "checked", true);
            }
          }
        } else if (this.noneSelected) {
          if (this.page === page) {
            for (let i in this.documents) {
              this.$set(this.documents[i], "checked", false);
            }
          }
          for (let i in this.loaded) {
            for (let j in this.loaded[i].documents) {
              this.$set(this.loaded[i].documents[j], "checked", false);
            }
          }
        }
      }
    }
  }
</script>

<style scoped>

</style>
