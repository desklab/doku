<template>
  <div class="border rounded p-4 bg-gray">
    <text-edit v-bind:text="stylesheet.name" v-bind:save="saveName" v-bind:placeholder="'Name'"></text-edit>
    <span v-if="isBase" class="chip bg-dark">
        base of &nbsp; <i>{{baseOfTemplate}}</i>
    </span>
    <span v-if="isEmpty" class="chip bg-error">
        empty source
    </span>
    <span v-if="!isUsed" class="chip bg-warning">
        unused
    </span>
    <span v-if="(isUsed)&&(!isBase)&&(numberOfUses>1)" class="chip text-success">
        used in {{numberOfUses}} templates
    </span>
    <span v-if="(isUsed)&&(!isBase)&&(numberOfUses==1)" class="chip text-success">
        used in {{numberOfUses}} template
    </span>
    <div class="btn-group btn-sm float-right">
      <animated-notice ref="notice"></animated-notice>
        <input ref="sourceFile" v-on:change="check_input" name="source" type="file" accept="text/css" class="mr-2">
        <button class="btn btn-sm mr-2" ref="updateButton"  :disabled="true" @click="upload">Update</button>
      <button class="btn btn-error btn-sm mr-2" :disabled="isEmpty" @click="clearStyleSource">Clear Source</button>
      <button class="btn btn-error btn-sm" :disabled="isBase" @click="deleteStyle">Delete</button>
    </div>
  </div>
</template>

<script>
  import {mapActions} from "vuex";
  import {MoreVerticalIcon, XIcon} from 'vue-feather-icons';
  import * as actionTypes from "../../store/types/actions";
  import AnimatedNotice from "../ui/AnimatedNotice";
  import TextEdit from "../ui/TextEdit";

  export default {
    name: 'StyleItem',
    props: {
      stylesheet: {
        type: Object
      }
    },
    components: {
      TextEdit,
      AnimatedNotice, MoreVerticalIcon, XIcon
    },
    computed: {
      baseOfTemplate: function(){
        if (this.stylesheet.base_templates[0])
          return this.stylesheet.base_templates[0].name
        else
          return null 
      },
      isBase: function() {
        if (this.stylesheet.base_templates[0])
          return true
        else
          return false 
      },
      isEmpty: function() {
        return this.stylesheet.source == null
      },
      isUsed: function() {
        if (this.stylesheet.templates.length > 0 || this.stylesheet.base_templates.length > 0)
          return true
        else
          return false
      },
      numberOfUses: function() {
        if (true)
          return this.stylesheet.templates.length
        else
          return null
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
      clearStyleSource(event) {
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
        if (this.$refs.sourceFile.files.length===0) {
          this.$refs.updateButton.disabled = true;
        } else {
          this.$refs.updateButton.disabled = false;
        }
      }
    },
  }
</script>

<style scoped>

</style>
