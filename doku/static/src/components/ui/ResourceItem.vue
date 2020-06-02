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
            <button class="btn btn-error btn-sm" @click="remove" >Remove</button>
        </div>
    </div>
</template>

<script>
  export default {
    methods: {
      remove(event) {
        this.removeResource(this.resource.id)         //TODO: is this.resource.id defined?
          .then(() => {window.location.href = '/';})
          .catch((err) => {
            console.error(err);
            this.$refs.deleteNotice.trigger('Failed!', 'text-error');
            event.target.classList.remove('loading');
          });
      }
    }
  }
</script>

<style scoped>

</style>
