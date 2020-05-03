<template>
  <modal ref="modal" class="modal-lg" v-bind:title="'Stylesheets'">
    <div class="modal-body">
      <div class="content">
        <StyleItem v-bind:stylesheet="template.base_style" v-bind:isBase="true" class="mb-2"></StyleItem>
        <StyleItem v-for="style in stylesheets" class="mb-2" v-bind:stylesheet="style" v-bind:isBase="false" v-bind:remove-url="template.remove_styles_url"></StyleItem>
      </div>
    </div>
    <div class="modal-footer">
      <div class="form-inline float-left">
        <select ref="select" name="template" class="form-select">
          <option value="">Create new</option>
          <option v-for="style in allStylesheets" :value="style.id">{{ style.name }}</option>
        </select>
      </div>
      <button @click="add" class="btn btn-primary ml-2 float-left">
        Add
      </button>
      <button @click="close" class="btn btn-link">
        Close
      </button>
    </div>
  </modal>
</template>

<script>
  import stylesheetApi from '../../api/stylesheet';
  import Modal from "./Modal";
  import StyleItem from "./StyleItem";
  import {mapActions, mapState} from "vuex";
  import * as actionTypes from "../../store/types/actions";

  export default {
    name: 'StylesheetModal',
    components: {Modal, StyleItem},
    computed: mapState({
      template: state => state.template.template,
      stylesheets: state => state.stylesheet.stylesheets
    }),
    data() {
      return {
        allStylesheets: []
      }
    },
    mounted() {
      stylesheetApi.fetchStylesheets().then(res => this.allStylesheets = res.data);
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
      }
    }
  }
</script>

<style scoped>

</style>
