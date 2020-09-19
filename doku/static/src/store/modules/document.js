import documentApi from '../../api/document';
import * as mutationTypes from '../types/mutations';

/**
 * Used to always include certain fields when updating/getting the
 * document.
 * @type {{params: {includes: [string, string, string]}}}
 */
const defaultConfig = {
  params: {
    includes: ['variables', 'variable_groups', 'root_variables']
  }
};

const state = {
  document: (window.documentObj !== undefined) ? JSON.parse(window.documentObj) : {},
  documentUpdateStatus: null
}

const getters = {
  documentVariables: state => {
    return state.document.variables;
  },
  documentRootVariables: state => {
    return state.document.root_variables;
  },
  documentGroups: state => {
    return state.document.variable_groups;
  }
}

const actions = {
  updateDocument({commit}, data) {
    return new Promise((resolve, reject) => {
      documentApi.updateDocument(data)
        .then(response => {
          commit(mutationTypes.SET_DOCUMENT, response.data);
          resolve();
        })
        .catch(reject)
    });
  },
  removeDocument({commit}, data) {
    return new Promise((resolve, reject) => {
      documentApi.removeDocument(data)
        .then(response => {
          resolve();
        })
        .catch(reject)
    });
  },
  fetchCurrentDocument({state, commit}) {
    return new Promise((resolve, reject) => {
      let documentId = state.document.id;
      documentApi.fetchDocument(documentId, defaultConfig)
        .then(response => {
          commit(mutationTypes.SET_DOCUMENT, response.data);
          resolve();
        }).catch(reject);
    })
  }
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
