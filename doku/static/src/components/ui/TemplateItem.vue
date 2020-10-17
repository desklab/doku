<template>
    <div class="column col-12 border rounded p-4 mb-2 bg-gray"> 
        <text-edit v-bind:text="template.name" v-bind:save="saveName" v-bind:placeholder="'Name'"></text-edit>
        <span v-if="(effectiveStylesCount>=1)" class="chip text-success">
          {{effectiveStylesCount}} non-empty styles
        </span>
        <span v-if="(numberOfUses==0)" class="chip text-warning">
          not in use
       </span>
        <span v-if="(numberOfUses==1)" class="chip text-success">
          used in {{numberOfUses}} document
       </span>
        <span v-if="(numberOfUses>1)" class="chip text-success">
          used in {{numberOfUses}} documents
       </span>
        <span class="float-right">
          <animated-notice ref="deleteNotice"></animated-notice>
          <a class="btn btn-sm ml-2" :href="template.id">Edit</a>
          <button class="btn btn-sm ml-2" @click="$refs.stylesModal.open()">Styles</button>
          <button class="btn btn-error btn-sm ml-2" @click="remove">Remove</button>
        </span>
        <StylesheetModal ref="stylesModal"></StylesheetModal>       
    </div>
</template>

<script>
  import templateApi from '../../api/resource';

  import * as actionTypes from '../../store/types/actions';
  import {mapState, mapActions} from 'vuex';

  import StylesheetModal from "./StylesheetModal";
  import AnimatedNotice from "./AnimatedNotice";
  import TextEdit from "./TextEdit";

  export default {
    components: {
      TextEdit,
      AnimatedNotice,
      StylesheetModal
    },
    computed: {
      effectiveStylesCount: function() {
        return this.template.id // ToDo: return number of stylesheets with not-empty src applied on this template
      },      
      numberOfUses: function() {
        return this.template.id // ToDo: return number of documents which use this template
      }
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
          url: this.template.update_url,
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
