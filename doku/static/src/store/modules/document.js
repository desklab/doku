import documentApi from '../../api/document';
import * as mutationTypes from '../types/mutations';

const state = {
  document: (window.documentObj !== undefined) ? JSON.parse(window.documentObj) : {},
  documentUpdateStatus: null
}

const getters = {}

const actions = {
  updateDocument({commit, state}, document) {
    return new Promise((resolve, reject) => {
      documentApi.updateDocument(document)
        .then(response => {
          commit(mutationTypes.SET_DOCUMENT, response.data)
        })
        .catch(reject);
    });
  },
}

const mutations = {
  setDocument(state, document) {
    Object.assign(state.document, document);
  },
  setDocumentTemplate(state, template) {
    Object.assign(state.document.template, template);
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
