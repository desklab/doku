<template>
  <div class="resize resize-vertical">
    <div class="resize-handle" @mousedown="resize" />
    <slot />
  </div>
</template>

<script>
export default {
  name: 'Resize',
  methods: {
    resize({pageX: initialPageX}) {
      let initialWidth = this.$el.offsetWidth;
      document.body.style.cursor = 'ew-resize';
      let move = ({pageX}) => {
        this.$el.style.width = initialWidth + (initialPageX - pageX) + 'px';
      };

      function end() {
        document.body.style.cursor = 'inherit';
        removeEventListener('mousemove', move);
        removeEventListener('mouseup', end);
      }

      addEventListener('mousemove', move);
      addEventListener('mouseup', end);
    }
  }
};
</script>

<style scoped>

</style>
