<template>
    <div class="container">
        <div class="border rounded p-4 m-3 bg-gray resource-form">
            <form action="" method="post" enctype="multipart/form-data">
                <label class="form-label d-inline-block text-small p-0 m-0" for="inputName">Name</label>
                <div class="form-inline mx-2">
                    <input class="form-input input-sm" type="text" name="name" id="inputName" placeholder="Name">
                </div>
                <input ref="sourceFile" name="file" type="file" accept="image/*">
                <button class="btn btn-sm btn-primary" @click="add">
                    Upload
                </button>
            </form>
        </div>
        <resource-item ref="resource_item" v-for="resource in resources" :key="resource.id" :resource="resource"></resource-item>
    </div>
</template>

<script>
    import resourceApi from '../api/resource';
    import ResourceItem from '../components/ui/ResourceItem';

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
    }
</script>

<style scoped>
</style>
