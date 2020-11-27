<template>
  <div class="pdf-document">
    <PDFPage
      v-for="page in pages"
      :key="page.pageNumber"
      v-bind="{page, scale}"
    />
  </div>
</template>

<script>
import PDFPage from './page.vue';
// Due to some change (what?), this does not work anymore
// import { pdfjs } from 'pdfjs-dist/build/pdf';
// Use require instead
// eslint-disable-next-line no-undef
let pdfjs = require('pdfjs-dist/build/pdf');
import PdfjsWorker from 'pdfjs-dist/build/pdf.worker';

pdfjs.GlobalWorkerOptions.workerPort = new PdfjsWorker();

export default {
  name: 'PDFDocument',
  components: {
    PDFPage,
  },
  props: ['url', 'scale'],
  data() {
    return {
      pdf: undefined,
      pages: []
    };
  },
  watch: {
    pdf(pdf) {
      this.pages = [];
      const promises = [
        // Create array of length pdf.numPages with indices
        ...Array(pdf.numPages).keys()
      ].map(number => pdf.getPage(number + 1));
      Promise.all(promises).then(pages => (this.pages = pages));
    },
  },
  methods: {
    fetchPDF(loader) {
      loader.classList.add('loading');
      pdfjs.getDocument(this.url).promise.then(pdf => {
        this.pdf = pdf;
        if (loader !== undefined) {
          loader.classList.remove('loading');
        }
      });
    },
  },
};
</script>

<style scoped>

</style>
