<template>
  <ul class="pagination">
    <li class="page-item" :class="pagination.has_prev ? '' : 'disabled'">
      <a :class="pagination.has_prev ? 'c-hand' : ''"
         tabindex="-1"
         @click="setPage(pagination.prev_num)"
      >
        <arrow-left-icon />
      </a>
    </li>
    <li v-for="p in pagination.pages"
        :key="p"
        :class="currentPage === p ? 'active' : ''"
        class="page-item"
    >
      <a v-if="p !== null && p !== undefined" class="c-hand" @click="setPage(p)">
        {{ p }}
      </a>
      <span v-else>...</span>
    </li>
    <li class="page-item" :class="pagination.has_next ? '' : 'disabled'">
      <a :class="pagination.has_next ? 'c-hand' : ''"
         @click="setPage(pagination.next_num)"
      >
        <arrow-right-icon />
      </a>
    </li>
  </ul>
</template>

<script>
import { ArrowLeftIcon, ArrowRightIcon } from 'vue-feather-icons';

export default {
  name: 'Pagination',
  components: {
    ArrowLeftIcon, ArrowRightIcon
  },
  props: {
    page: {
      type: Number,
      default: 1
    },
    pagination: {
      type: Object,
      default: undefined
    },
    // TODO change to event
    // eslint-disable-next-line vue/require-default-prop
    callback: {
      type: Function
    }
  },
  data() {
    return {
      currentPage: this.page
    };
  },
  watch: {
    page: function (newPage) {
      this.currentPage = newPage;
    },
  },
  methods: {
    setPage(p) {
      this.currentPage = p;
      this.callback(this.currentPage);
    }
  }
};
</script>

<style scoped>

</style>
