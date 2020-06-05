import resourceApi from '../../api/resource';
import * as mutationTypes from '../types/mutations';
import * as actionTypes from '../types/actions';

const state = {
  resources: (window.resources !== undefined) ? JSON.parse(window.resources) : [],
}

const getters = {}

const actions = {
  uploadResource({commit, state}, data) {
    return new Promise((resolve, reject) => {
      if (!data.hasOwnProperty('url')) {
        throw Error('Missing url');
      }
      if (!data.hasOwnProperty('formData')) {
        throw Error('Missing form data');
      }
      resourceApi.uploadResource(data.url, data.formData)
        .then(response => {
          commit(mutationTypes.SET_RESOURCE, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  fetchResource({commit, state}, options) {
    options = options || {};
    return new Promise((resolve, reject) => {
      resourceApi.fetchResource(options)
        .then(response => {
          commit(mutationTypes.SET_RESOURCES, response.data);
          resolve();
        })
        .catch(reject)
    });
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions
}
