<template>
    <div class="column col-12 resource-item border rounded p-4 mb-2 bg-gray">
        <div class="resource-res">
            <img :src="resource.url" alt="...">
        </div>
        <div class="resource-desc">
            <span class="ml-2"><b>{{ resource.name }}</b></span>
            <span class="ml-2">
                <b>Usage:</b> <code>![{{ resource.name }}](dokures:{{ resource.filename }})</code>
            </span>
        </div>
        <div class="resource-end">
            <animated-notice ref="deleteNotice"></animated-notice>
            <button class="btn btn-error btn-sm" @click="remove" >Remove</button>
        </div>
    </div>
</template>

<script>
  import * as actionTypes from '../../store/types/actions';
  import {mapState, mapActions} from 'vuex';
  import AnimatedNotice from "./AnimatedNotice";

  export default {
    components: {
      AnimatedNotice
    },
    methods: {
      ...mapActions('resource', [
        actionTypes.REMOVE_RESOURCE,
      ]),
      remove(event) {
        event.target.classList.add('loading');
        let data = {
          	url: this.resource.delete_url,
            id: this.resource.id
        }
        this.removeResource(data)
          .catch((err) => {
            console.error(err);
            this.$refs.deleteNotice.trigger('Failed!', 'text-error');
            event.target.classList.remove('loading');
          });
      }
    },
    props: ['resource']
  }
</script>

<style scoped>

</style>
