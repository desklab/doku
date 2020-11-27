<template>
  <div>
    <resource-item
      v-for="resource in resources" ref="resource_item"
      :key="resource.id"
      :resource="resource"
    />
  </div>
</template>

<script>
import resourceApi from '../api/resource';
import ResourceItem from '../components/resource/ResourceItem';

import {mapState, mapActions} from 'vuex';
import * as actionTypes from '../store/types/actions';


export default {
  name: 'Resources',
  components: {
    ResourceItem
  },
  computed: mapState({
    resources: state => state.resource.resources
  }),
  methods: {
    ...mapActions('resource', [
      actionTypes.CREATE_RESOURCE,
    ]),
    add() {
      let url = this.add_resource_url;
      resourceApi.createResource({name: 'New Resource'})
        .then(res => {
          this.addResourc({url: url, data: {id: res.data.id}});
        });
    }
  }
};
</script>

<style scoped>
</style>
