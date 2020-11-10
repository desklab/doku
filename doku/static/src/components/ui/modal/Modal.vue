<template>
  <div class="modal">
    <a @click="close" class="modal-overlay" aria-label="Close"></a>
    <div class="modal-container">
      <div class="modal-header">
        <a @click="close" class="btn btn-clear float-right" aria-label="Close"></a>
        <div class="modal-title h5">{{ title }}</div>
      </div>
      <slot></slot>
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
      close() {
        this.$el.classList.remove('active');
      }
    }
  }
</script>

<style scoped>

</style>
