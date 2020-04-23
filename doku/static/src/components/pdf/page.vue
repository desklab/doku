<template>
  <div>
    <div ref="svg" class="doku-edit-page" style="width: 100%"></div>
  </div>
</template>

<script>
  import pdfjs from 'pdfjs-dist';


  export default {
    props: ['page', 'scale'],
    name: 'PDFPage',
    render(h) {
      const {canvasAttrs: attrs} = this;
      return h('canvas', {attrs});
    },
    created() {
      this.viewport = this.page.getViewport({scale: this.scale});
    },
    mounted() {
      this.drawPage();
    },
    methods: {
      drawPage() {
        if (this.renderTask) return;
        this.renderTask = this.page.getOperatorList();
        this.renderTask.then((opList) => {
          let svgGfx = new pdfjs.SVGGraphics(this.page.commonObjs, this.page.objs);
          return svgGfx.getSVG(opList, this.viewport);
        }).then((svg) => {
          svg.setAttribute('width', '100%');
          svg.removeAttribute('height');
          this.$refs.svg.appendChild(svg);
        });
      },
      destroyPage(page) {
        if (!page) return;
        page._destroy();
        if (this.renderTask) {
          this.renderTask.cancel();
          delete this.renderTask;
        }
      },
    },
    watch: {
      page(page, oldPage) {
        this.destroyPage(oldPage);
      }
    },
  }
</script>

<style scoped>

</style>
