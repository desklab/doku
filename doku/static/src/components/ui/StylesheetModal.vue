<template>
  <modal ref="modal" title="Stylesheet Selection">
    <div class="modal-body">
      <div class="content">
        <div class="d-block text-right">
          <button @click="selectNone" class="btn btn-sm">
            Deselect All
          </button>
        </div>
        <div>
          <div v-for="style in stylesheets" :key="style.id" class="form-group">
            <label class="form-checkbox c-hand">
              <input type="checkbox" @change="select(style.id, $event)" :checked="selection.has(style.id)" :disabled="loading">
              <i class="form-icon"></i> {{ style.name }}
            </label>
          </div>
        </div>
        <pagination :page="this.page" :pagination="pagination" :callback="setPage"></pagination>
      </div>
    </div>
    <div class="modal-footer">
      <a href="/stylesheets" class="btn btn-link float-left">
        Manage Stylesheets
      </a>
      <animated-notice ref="downloadNotice"></animated-notice>
      <button @click="close" class="btn btn-link">
        Close
      </button>
    </div>
  </modal>
</template>

<script>
  import stylesheetApi from '../../api/stylesheet';
  import Modal from "./Modal";
  import Pagination from './Pagination.vue';
  import AnimatedNotice from "./AnimatedNotice";
  import {mapActions, mapState} from "vuex";
  import * as actionTypes from "../../store/types/actions";

  export default {
    name: 'StylesheetModal',
    components: {Modal, Pagination, AnimatedNotice},
    computed: mapState({
      template: state => state.template.template
    }),
    data() {
      return {
        allStylesheets: [],
        stylesheets: [],
        selection: new Set(),
        pagination: {
          has_next: false,
          has_prev: false,
          pages: []
        },
        page: 1,
        loaded: {},
        noneSelected: false,
        loading: false,
        returnToOldPage: -1
      }
    },
    mounted() {
      stylesheetApi.fetchStylesheets().then(res => this.allStylesheets = res.data.result);
    },
    methods: {
      ...mapActions('template', [
        actionTypes.ADD_STYLESHEET_TO_TEMPLATE,
      ]),
      toggle() {
        this.$refs.modal.toggle();
      },
      open() {
        this.$refs.modal.open();
      },
      close() {
        this.$refs.modal.close();
      },
      add() {
        let stylesheet_id = this.$refs.select.value;
        let url = this.template.add_styles_url;
        if (stylesheet_id === "") {
          stylesheetApi.createStylesheet({name: 'New Stylesheet'})
            .then(res => {
              this.addStylesheet({url: url, data: {id: res.data.id}});
            });
        } else {
          this.addStylesheet({url: url, data: {id: stylesheet_id}});
        }
      },
      setPage(p) {
        // Update the current page
        this.$set(this.loaded, this.page, {
          stylesheets: this.stylesheets,
          pagination: this.pagination
        });
        // Change the page
        this.page = p;
        // Fetch or update stylesheets and pagination objects
        this.update();
      },
      selectionChanged() {
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
          stylesheetApi.fetchStylesheets({params: {page: page}})
            .then(res => {
              this.$set(this.loaded, page, {
                stylesheets: res.data.result,
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
            this.stylesheets = this.loaded[this.page].stylesheets;
            this.pagination = this.loaded[this.page].pagination;
          });
      },
      selectNone(event) {
        event.target.classList.add("loading");
        this.noneSelected = true;

        this.selection = new Set();

        event.target.classList.remove("loading");
      },
    }
  }
</script>

<style scoped>

</style>
