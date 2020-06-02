<template>
    <div class="container">
        <div class="border rounded p-4 m-3 bg-gray resource-form">
            <form action="" method="post" enctype="multipart/form-data">
                <label class="form-label d-inline-block text-small p-0 m-0" for="inputName">Name</label>
                <input type="hidden" name="csrf_token" :value="create_csrf_token()"/>
                <div class="form-inline mx-2">
                    <input class="form-input input-sm" type="text" name="name" id="inputName" placeholder="Name">
                </div>
                <input ref="sourceFile" name="file" type="file" accept="image/*">
                <button type="submit" class="btn btn-sm btn-primary ">Upload
                </button>
            </form>
        </div>
    </div>
</template>

<script>
    import ResourceItem from '../components/ui/ResourceItem';

    export default {
      name: 'Resources'
    }
</script>

<style scoped>
</style>
