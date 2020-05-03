<template>
  <div class="border rounded p-4 bg-gray">
    <text-edit v-bind:text="stylesheet.name" v-bind:save="saveName" v-bind:placeholder="'Name'"></text-edit>
    <span v-if="isBase" class="chip">
        Base
    </span>
    <input ref="sourceFile" name="source" type="file" accept="text/css">
    <div class="btn-group btn-sm float-right">
      <animated-notice ref="notice"></animated-notice>
      <button @click="upload" class="btn btn-sm btn-primary float-right">Upload</button>
      <button @click="remove" v-if="!isBase" class="btn btn-sm" tabindex="0">
        <x-icon size="16"></x-icon>
      </button>
    </div>
  </div>
</template>

<script>
  import {mapActions} from "vuex";
  import {MoreVerticalIcon, XIcon} from 'vue-feather-icons';
  import * as actionTypes from "../../store/types/actions";
  import AnimatedNotice from "./AnimatedNotice";
  import TextEdit from "./TextEdit";

  export default {
    name: 'StyleItem',
    props: {
      stylesheet: {
        type: Object
      },
      isBase: {
        type: Boolean,
        default: false
      },
      isUsed: {
        type: Boolean,
        default: false
      },
      removeUrl: {
        type: String
      }
    },
    components: {
      TextEdit,
      AnimatedNotice, MoreVerticalIcon, XIcon
    },
    methods: {
      ...mapActions('stylesheet', [
        actionTypes.UPLOAD_STYLESHEET,
        actionTypes.UPDATE_STYLESHEET
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
      },
      remove(event) {
        event.target.classList.add('loading');
        let data = {
          url: this.removeUrl,
          data: {
            id: this.stylesheet.id
          }
        };
        this.removeStylesheet(data)
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
      }
    },
  }
</script>

<style scoped>

</style>
