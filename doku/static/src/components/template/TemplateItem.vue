<template>
    <div class="column col-12 border rounded p-4 mb-2 bg-gray"> 
        <text-edit v-bind:text="template.name" v-bind:save="saveName" v-bind:placeholder="'Name'"></text-edit>
        <span v-if="(numberOfStyles>=1)" class="chip bg-dark">
          {{numberOfStyles}} stylesheets
        </span>
        <span class="float-right">
            <animated-notice ref="deleteNotice"></animated-notice>
            <a class="btn btn-sm ml-2" :href="template.id">Edit Source</a>
            <button class="btn btn-sm ml-2" @click="$refs.stylesSelector.open()">Select Styles</button>
            <button class="btn btn-error btn-sm ml-2" @click="remove">Remove</button>
        </span>
        <multi-select-modal ref="stylesSelector" title="Select Stylesheets" :api-fetch="stylesheetApiFetch" :defaultSelection="selectedStylesheets" :none="false" :editLink="'../stylesheets'" v-on:doku-selection-made="setSelectedStylesheets"></multi-select-modal>      
    </div>
</template>

<script>
  import templateApi from '../../api/resource';
  import stylesheetApi from '../../api/stylesheet';

  import * as actionTypes from '../../store/types/actions';
  import {mapState, mapActions} from 'vuex';

  import AnimatedNotice from "../ui/AnimatedNotice";
  import TextEdit from "../ui/form/TextEdit";
  import MultiSelectModal from "../ui/modal/MultiSelectModal";

  export default {
    components: {
      TextEdit,
      AnimatedNotice,
      MultiSelectModal
    },
    computed: {
      numberOfStyles: function() {
        return this.template.styles.length
      },
      selectedStylesheets: function () {
        let stylesheetIDs = [];
        for (let i in this.template.styles) {
          stylesheetIDs.push(this.template.styles[i].id);
        }
        return stylesheetIDs;
      }
    },
    data() {
      return {
        stylesheetApiFetch: stylesheetApi.fetchStylesheets
      }
    },
    methods: {
      ...mapActions('template', [
        actionTypes.REMOVE_TEMPLATE,
        actionTypes.UPDATE_TEMPLATE
      ]),
      ...mapActions('stylesheet', [
        actionTypes.SET_STYLESHEETS_FOR_TEMPLATE,
      ]),
      remove(event) {
        event.target.classList.add('loading');
        this.removeTemplate(this.template.delete_url, this.template.id)
          .then(() => {
            // ToDo: fetch and update templates
          })
          .catch((err) => {
            console.error(err);
            this.$refs.deleteNotice.trigger('Failed!', 'text-error');
          })
          .finally(() => {
            event.target.classList.remove('loading');
          });
      },
      saveName(name) {
        let data = {
          url: this.template.url,
          id: this.template.id,
          name: name
        };
        this.updateTemplate(data)
          .then(() => {
            // ToDo: fetch and update templates
          })            
          .catch(err => {
            console.error(err);
          });
      },
      setSelectedStylesheets(selectedIDs) {
        let selectedStylesheetObjects = [];
        for (let i in selectedIDs) {
          selectedStylesheetObjects.push({
            id: selectedIDs[i]
          });
        }
        this.updateTemplate({
          id: this.template.id,
          styles: selectedStylesheetObjects
        })
      },
    },
    props: ['template']
  }
</script>

<style scoped>

</style>
