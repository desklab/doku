<template>
  <ul class="pagination">
    <li class="page-item" :class="pagination.has_prev ? '' : 'disabled'">
      <a @click="setPage(pagination.prev_num)" :class="pagination.has_prev ? 'c-hand' : ''" tabindex="-1">
        <arrow-left-icon></arrow-left-icon>
      </a>
    </li>
    <li v-for="p in pagination.pages" v-bind:key="p" :class="(currentPage == p) ? 'active' : ''" class="page-item">
      <a v-if="p !== null && p !== undefined" class="c-hand" @click="setPage(p)">{{ p }}</a>
      <span v-else>...</span>
    </li>
    <li class="page-item" :class="pagination.has_next ? '' : 'disabled'">
      <a @click="setPage(pagination.next_num)" :class="pagination.has_next ? 'c-hand' : ''">
        <arrow-right-icon></arrow-right-icon>
      </a>
    </li>
  </ul>
</template>

<script>
  import { ArrowLeftIcon, ArrowRightIcon } from 'vue-feather-icons';

  export default {
    name: 'Pagination',
    props: ['page', 'pagination', 'callback'],
    components: {
      ArrowLeftIcon, ArrowRightIcon
    },
    data() {
      return {
        currentPage: this.page
      }
    },
    methods: {
      setPage(p) {
        this.currentPage = p;
        this.callback(this.currentPage);
      }
    },
    watch: {
      page: function (newPage, oldPage) {
        this.currentPage = newPage;
      },
    }
  }
</script>

<style scoped>

</style>
