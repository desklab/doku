<template>
  <resize>
    <div class="doku-preview">
      <div class="doku-preview-toolbar">
        <button ref="loader" class="btn btn-sm btn-link text-dark" @click="refresh">
          Refresh
        </button>
        <a :href="url" class="btn btn-sm btn-link-icon">
          <download-icon />
        </a>
      </div>
      <PDFDocument ref="document" class="doku-preview-document" v-bind="{url, scale}" />
    </div>
  </resize>
</template>

<script>
import { DownloadIcon } from 'vue-feather-icons';

import PDFDocument from './document.vue';
import resize from '../ui/Resize';


export default {
  name: 'App',
  components: {
    PDFDocument, resize, DownloadIcon
  },
  props: [
    'url'
  ],
  data() {
    return {
      scale: 1
    };
  },
  mounted() {
    this.$refs.document.fetchPDF(this.$refs.loader);
  },
  methods: {
    refresh(event) {
      this.$refs.document.fetchPDF(event.target);
    }
  }
};
</script>

<style scoped>

</style>
