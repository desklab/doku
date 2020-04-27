import documentApi from '../../api/document';
import templateApi from '../../api/template';
import * as mutationTypes from '../types/mutations';
import * as actionTypes from '../types/actions';

const state = {
  document: (window.documentObj !== undefined) ? JSON.parse(window.documentObj) : {},
  documentUpdateStatus: null
}

const getters = {}

/**
 * Remove Variable
 *
 * Uses filter to remove a variable from the document.
 *
 * @param variable: The variable that should be tested
 * @param test: Note: This has to pass for the variable to be removed
 * @returns {boolean}
 */
const removeVariable = function (variable, test) {
  if (test(variable)) {
    return false
  }
  if (variable.is_list) {
    variable.children = variable.children.filter(v => removeVariable(v, test))
  }
  return true
}

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
  updateVariables({commit, state}, variables) {
    return new Promise((resolve, reject) => {
      documentApi.updateVariables(variables)
        .then(response => {
          commit(mutationTypes.SET_VARIABLES, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  updateVariable({commit, state}, variable) {
    return new Promise((resolve, reject) => {
      documentApi.updateVariables(variable)
        .then(response => {
          commit(mutationTypes.SET_VARIABLE, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  removeVariable({commit, state}, variableId) {
    return new Promise((resolve, reject) => {
      documentApi.removeVariable(variableId)
        .then(() => {
          commit(mutationTypes.REMOVE_VARIABLE, variableId);
          resolve();
        })
        .catch(reject);
    });
  },
  fetchVariables({commit, state}, options) {
    options = options || {};
    return new Promise((resolve, reject) => {
      documentApi.fetchVariables(options)
        .then(response => {
          commit(mutationTypes.SET_VARIABLES, response.data);
          resolve();
        })
        .catch(reject)
    });
  },
  updateDocumentTemplate({commit, state, dispatch}, template) {
    return new Promise((resolve, reject) => {
      templateApi.updateTemplate(template)
        .then(response => {
          let oldVariables = (state.document.variables || []).map(v => v.name);
          commit(mutationTypes.SET_DOCUMENT_TEMPLATE, response.data);
          let hasMissing = response.data.available_fields.some(
            field => !oldVariables.includes(field)
          );
          if (hasMissing) {
            let options = {
              document_id: state.document.id
            }
            dispatch(actionTypes.FETCH_VARIABLES, options)
              .then(resolve)
              .catch(reject);
          } else {
            resolve();
          }
        })
        .catch(reject)
    });
  }
}

const mutations = {
  setDocument(state, document) {
    Object.assign(state.document, document);
  },
  setVariables(state, variables) {
    state.document.variables = variables;
  },
  removeVariable(state, variableId) {
    state.document.variables = state.document.variables.filter(
      variable => removeVariable(variable, v => v.id === variableId)
    );
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
