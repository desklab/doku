<template>
  <div class="border rounded p-4 bg-gray">
    {{ stylesheet.name }}
    <span v-if="isBase" class="chip">
        Base
    </span>
    <input ref="sourceFile" name="source" type="file" size="50" accept="text/*">
    <button @click="save" class="btn btn-sm btn-primary float-right">Save</button>
  </div>
</template>

<script>
  import axios from "axios";

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
      }
    },
    methods: {
      save(event) {
        event.target.classList.add('loading');
        let formData = new FormData();
        formData.append('source', this.$refs.sourceFile.files[0]);
        axios
          .put(this.stylesheet.update_url, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .finally(() => {
            event.target.classList.remove('loading');
          });
      }
    }
  }
</script>

<style scoped>

</style>
