<template>
  <div class="doku-animated-toggle">
    <label class="form-switch">
      <input v-model="checked" id="documentPublicInput" type="checkbox">
      <i class="form-icon"></i>
      <transition name="slide-down">
        <span v-if="checked">
          <slot name="on"></slot>
        </span>
      </transition>
      <transition name="slide-up">
        <span v-if="!checked">
          <slot name="off"></slot>
        </span>
      </transition>
    </label>
  </div>
</template>

<script>
  export default {
    name: 'AnimatedToggle',
    props: {
      isChecked: Boolean,
      onCheck: {
        type: Function,
        default: () => {
        }
      }
    },
    data() {
      return {
        checked: this.isChecked,
      }
    },
    methods: {
      toggle() {
        this.checked = !this.checked;
      },
    },
    watch: {
      checked: 'onCheck'
    }
  }
</script>

<style scoped>
</style>
