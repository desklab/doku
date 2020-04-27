<template>
  <transition name="fade-out">
    <span v-if="$data._show" :class="$data._cssClasses" class="mr-2">
      {{$data._text}}
    </span>
  </transition>
</template>

<script>
  export default {
    name: 'AnimatedNotice',
    data() {
      return {
        _text: '',
        _cssClasses: '',
        _show: false
      }
    },
    methods: {
      trigger(text, cssClasses, duration = 2000) {
        this.$data._text = text;
        this.$data._cssClasses = cssClasses;
        this.$data._show = true;
        setTimeout(() => {
          this.$data._show = false
        }, duration);
      }
    }
  }
</script>

<style scoped>

</style>
