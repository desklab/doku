<template>
  <div class="border rounded p-4 bg-gray">
    {{ stylesheet.name }}
    <span v-if="isBase" class="chip">
        Base
    </span>
    <input ref="sourceFile" name="source" type="file" size="50" accept="text/*">
    <button @click="upload" class="btn btn-sm btn-primary float-right">Upload</button>
  </div>
</template>

<script>
  import axios from "axios";
  import {mapActions} from "vuex";
  import * as actionTypes from "../../store/types/actions";

  axios.defaults.xsrfCookieName = 'csrf_token';
  axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';

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
      }
    },
    methods: {
      ...mapActions('stylesheet', [
        actionTypes.UPLOAD_STYLESHEET
      ]),
      upload(event) {
        event.target.classList.add('loading');
        let formData = new FormData();
        formData.append('source', this.$refs.sourceFile.files[0]);
        this.uploadStylesheet({
          url: this.stylesheet.upload_url,
          formData: formData
        }).finally(() => {
          event.target.classList.remove('loading');
        });
      }
    },
  }
</script>

<style scoped>

</style>
