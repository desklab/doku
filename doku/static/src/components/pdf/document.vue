<template>
  <div class="pdf-document">
    <PDFPage
      v-for="page in pages"
      v-bind="{page, scale}"
      :key="page.pageNumber"
    />
  </div>
</template>

<script>
  import PDFPage from './page.vue';
  import range from 'lodash/range';
  // Due to some change (what?), this does not work anymore
  // import { pdfjs } from 'pdfjs-dist/build/pdf';
  // Use require instead
  let pdfjs = require('pdfjs-dist/build/pdf');
  import PdfjsWorker from 'pdfjs-dist/build/pdf.worker';

  pdfjs.GlobalWorkerOptions.workerPort = new PdfjsWorker();

  export default {
    props: ['url', 'scale'],
    name: 'PDFDocument',
    components: {
      PDFPage,
    },
    data() {
      return {
        pdf: undefined,
        pages: []
      };
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
    watch: {
      pdf(pdf) {
        this.pages = [];
        const promises = range(1, pdf.numPages + 1).map(number => pdf.getPage(number));
        Promise.all(promises).then(pages => (this.pages = pages));
      },
    },
  }
</script>

<style scoped>

</style>
