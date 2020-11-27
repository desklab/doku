<template>
  <div class="modal">
    <a class="modal-overlay" aria-label="Close" @click="close" />
    <div class="modal-container">
      <div class="modal-header">
        <a class="btn btn-clear float-right" aria-label="Close" @click="close" />
        <div class="modal-title h5">
          {{ title }}
        </div>
      </div>
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',
  props: ['title'],
  methods: {
    toggle() {
      this.$el.classList.toggle('active');
    },
    open() {
      this.$el.classList.add('active');
    },
    show() {
      this.open();
    },
    close() {
      this.$el.classList.remove('active');
    }
  }
};
</script>

<style scoped>

</style>
