<template>
  <div class="resize resize-vertical">
    <div class="resize-handle" v-on:mousedown="resize"></div>
    <slot></slot>
  </div>
</template>

<script>
  export default {
    name: 'Resize',
    methods: {
      resize({target: target, pageX: initialPageX, pageY: initialPageY}) {
        let initialWidth = this.$el.offsetWidth;
        document.body.style.cursor = 'ew-resize';
        let move = ({pageX, pageY}) => {
          this.$el.style.width = initialWidth + (initialPageX - pageX) + 'px';
        }

        function end() {
          document.body.style.cursor = 'inherit';
          removeEventListener('mousemove', move);
          removeEventListener('mouseup', end);
        }

        addEventListener('mousemove', move);
        addEventListener('mouseup', end);
      }
    }
  }
</script>

<style scoped>

</style>
