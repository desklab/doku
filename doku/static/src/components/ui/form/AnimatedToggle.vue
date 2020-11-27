<template>
  <div class="doku-animated-toggle">
    <label class="form-switch">
      <input type="hidden" :name="inputName" :value="hiddenInputValue">
      <input id="documentPublicInput" v-model="checked" type="checkbox">
      <i class="form-icon" />
      <transition name="slide-down">
        <span v-if="checked">
          <slot name="on" />
        </span>
      </transition>
      <transition name="slide-up">
        <span v-if="!checked">
          <slot name="off" />
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
    },
    inputName: String
  },
  data() {
    return {
      checked: this.isChecked,
    };
  },
  computed: {
    hiddenInputValue() {
      return (this.checked) ? 'on' : 'off';
    }
  },
  watch: {
    checked: 'onCheck'
  },
  methods: {
    toggle() {
      this.checked = !this.checked;
    },
  }
};
</script>

<style scoped>
</style>
