<template>
    <div class="column col-12 resource-item border rounded p-4 mb-2 bg-gray">
        <div class="resource-res">
            <img :src="resource.url" alt="...">
        </div>
        <div class="resource-desc">
            <span class="ml-2">
                <b>Name:</b>
                <text-edit v-bind:text="resource.name" v-bind:save="saveName" v-bind:placeholder="'Name'"></text-edit>
            </span>
            <span class="ml-2">
                <b>Usage:</b> <code :id="'includeLink'+String(resource.id)">{{includeLink}}</code>
            </span>
        </div>
        <div class="resource-end">
            <animated-notice ref="deleteNotice"></animated-notice>
            <button class="btn btn-sm" :data-clipboard-target="'#includeLink'+String(resource.id)" :id="'copy'+String(resource.id)">Copy Link</button>
            <button class="btn btn-error btn-sm" @click="remove">Remove</button>
        </div>
    </div>
</template>

<script>
  import resourceApi from '../../api/resource';
  import * as actionTypes from '../../store/types/actions';
  import {mapState, mapActions} from 'vuex';
  import AnimatedNotice from "../ui/AnimatedNotice";
  import TextEdit from "../ui/TextEdit";
  import ClipboardJS from 'clipboard';

  export default {
    components: {
      TextEdit,
      AnimatedNotice
    },
    computed: {
      includeLink: function() {
        return '![' + this.resource.name + '](dokures:' + this.resource.filename + ')'
      }
    },
    mounted() {
      var copyLink = new ClipboardJS('#copy' + String(this.resource.id), {
        text: () => '![' + this.resource.name + '](dokures:' + this.resource.filename + ')'
      });
      copyLink.on('success', function(event) {
        event.clearSelection();
      });
    },
    methods: {
      ...mapActions('resource', [
        actionTypes.REMOVE_RESOURCE,
        actionTypes.UPDATE_RESOURCE
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
      },
      saveName(name) {
        let data = {
          id: this.resource.id,
          name: name
        };
        this.updateResource(data)
          .catch(err => {
            console.error(err);
          });
      }
    },
    props: ['resource']
  }
</script>

<style scoped>

</style>
