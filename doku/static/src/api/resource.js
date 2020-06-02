import {axiosInstance as axios} from './index';

const RESOURCE_API = window.resourceApi || '/api/v1/resource/';

export default {
  updateResource(resource) {
    return axios.put(RESOURCE_API, resource);
  },
  createResource(resource) {
    return axios.post(RESOURCE_API, resource);
  },
  removeResource(resourceId) {
    return axios.delete(`${RESOURCE_API}${resourceId}/`);
  },
  fetchResource(options) {
    return axios.get(RESOURCE_API, {params: options});
  }
}
