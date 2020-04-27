<template>
  <resize>
    <div class="doku-preview">
      <div class="doku-preview-toolbar">
        <button ref="loader" @click="refresh" class="btn btn-sm btn-link text-dark">
          Refresh
        </button>
        <a v-bind:href="url" class="btn btn-sm btn-link-icon">
          <download-icon></download-icon>
        </a>
      </div>
      <PDFDocument ref="document" class="doku-preview-document" v-bind="{url, scale}"/>
    </div>
  </resize>
</template>

<script>
  import { DownloadIcon } from 'vue-feather-icons';

  import PDFDocument from './document.vue';
  import resize from "../ui/Resize";


  export default {
    name: 'app',
    components: {
      PDFDocument, resize
      PDFDocument, resize, DownloadIcon
    },
    data() {
      return {
        url: window.renderUrl,
        scale: 1
      }
    },
    mounted() {
      this.$refs.document.fetchPDF(this.$refs.loader)
    },
    methods: {
      refresh(event) {
        this.$refs.document.fetchPDF(event.target);
      }
    }
  }
</script>

<style scoped>

</style>
