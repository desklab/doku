<template>
    <div class="column col-12 resource-item border rounded p-4 mb-2 bg-gray">
        {{ template.id }}, {{ template.name }}             
        <animated-notice ref="deleteNotice"></animated-notice>
        <button class="btn btn-error btn-sm" @click="remove">Remove</button>
    </div>
</template>

<script>
  import templateApi from '../../api/resource';
  import * as actionTypes from '../../store/types/actions';
  import {mapState, mapActions} from 'vuex';
  import AnimatedNotice from "./AnimatedNotice";
  import TextEdit from "./TextEdit";

  export default {
    components: {
      TextEdit,
      AnimatedNotice
    },
    methods: {
      ...mapActions('template', [
        actionTypes.REMOVE_TEMPLATE,
        actionTypes.UPDATE_TEMPLATE
      ]),
      remove(event) {
        event.target.classList.add('loading');
        let data = {
          	url: this.template.delete_url,
            id: this.template.id
        }
        this.removeTemplate(data)
          .catch((err) => {
            console.error(err);
            this.$refs.deleteNotice.trigger('Failed!', 'text-error');
            event.target.classList.remove('loading');
          });
      },
      saveName(name) {
        let data = {
          id: this.template.id,
          name: name
        };
        this.updateTemplate(data)
          .catch(err => {
            console.error(err);
          });
      }
    },
    props: ['template']
  }
</script>

<style scoped>

</style>
