<template>
  <transition name="fade-out">
    <span v-if="show" :class="cssClasses" class="mr-2">
      {{ text }}
    </span>
  </transition>
</template>

<script>
export default {
  name: 'AnimatedNotice',
  data() {
    return {
      text: '',
      cssClasses: '',
      show: false
    };
  },
  methods: {
    trigger(text, cssClasses, duration = 2000) {
      this.text = text;
      this.cssClasses = cssClasses;
      this.show = true;
      setTimeout(() => {
        this.show = false;
      }, duration);
    }
  }
};
</script>

<style scoped>

</style>
