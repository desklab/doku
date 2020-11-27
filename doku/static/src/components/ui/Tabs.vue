<template>
  <ul class="tab">
    <li
      v-for="(tab, index) in tabs"
      :key="tab.title"
      class="tab-item"
      :class="tab.active ? 'active' : ''"
    >
      <a :href="`#${index}`" @click="openTab(index)">
        {{ tab.title }}
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'Tabs',
  props: {
    tabs: {
      type: Array,
      default: null
    },
    selectedTab: {
      type: Number,
      default: undefined
    }
  },
  mounted() {
    if (
      this.selectedTab !== undefined
      && 0 <= this.selectedTab
      && this.currentTab < this.tabs.length
    ) {
      this.currentTab = this.selectedTab;
    } else {
      let hash = window.location.hash;
      if (hash !== undefined && hash !== '' && hash.startsWith('#')) {
        this.currentTab = Number(hash.substring(1));
        if (
          isNaN(this.currentTab)
          || this.currentTab > this.tabs.length
          || this.currentTab < 0
        )
          this.currentTab = 0;
      } else {
        this.currentTab = 0;
      }
    }
    // TODO fix mutation of property
    this.tabs[this.currentTab].active = true;
  },
  methods: {
    openTab(index) {
      this.tabs[this.currentTab].active = false;
      this.tabs[index].active = true;
      this.currentTab = index;
    }
  }
};
</script>

<style scoped>

</style>
