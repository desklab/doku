import variableApi from '../../api/variable';
import * as mutationTypes from '../types/mutations';
import * as actionTypes from '../types/actions';
import * as ns from '../namespace';

const state = {}

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
  /**
   * Update Variables
   *
   * Instead of using mutations, the state is handled by the document
   * store. It is updated by calling `fetchCurrentDocument`.
   *
   * @param dispatch - Supplied by Vuex (used to dispatch Document action)
   * @param variables - (List of) objects that describe the updated variables
   * @returns {Promise<void>}
   */
  updateVariables({dispatch}, variables) {
    return new Promise((resolve, reject) => {
      variableApi.updateVariables(variables)
        .then(response => {
          dispatch(
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT)
          ).then(resolve).catch(reject);
        })
        .catch(reject);
    });
  },

  /**
   * Update a single Variable
   *
   * Instead of using mutations, the state is handled by the document
   * store. It is updated by calling `fetchCurrentDocument`.
   *
   * @param dispatch - Supplied by Vuex (used to dispatch Document action)
   * @param variable - Objects that describe the updated variable
   * @returns {Promise<void>}
   */
  updateVariable({dispatch}, variable) {
    return new Promise((resolve, reject) => {
      variableApi.createVariable(variable)
        .then(response => {
          dispatch(
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT)
          ).then(resolve).catch(reject);
        })
        .catch(reject);
    });
  },

  /**
   * Create Variable
   *
   * Creates a new variable based on the supplied parameter.
   *
   * Instead of using mutations, the state is handled by the document
   * store. It is updated by calling `fetchCurrentDocument`.
   *
   * @param dispatch - Supplied by Vuex (used to dispatch Document action)
   * @param variable - Objects that describe the new variable
   * @returns {Promise<void>}
   */
  createVariable({dispatch}, variable) {
    return new Promise((resolve, reject) => {
      variableApi.createVariable(variable)
        .then(response => {
          dispatch(
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT)
          ).then(resolve).catch(reject);
        })
        .catch(reject);
    });
  },

  /**
   * Remove Variable
   *
   * This will remove a variable (i.e. delete) from the document. It will
   * no longer be accessible.
   *
   * Instead of using mutations, the state is handled by the document
   * store. It is updated by calling `fetchCurrentDocument`.
   *
   * @param dispatch - Supplied by Vuex (used to dispatch Document action)
   * @param variableId - ID for the variable to be deleted
   * @returns {Promise<void>}
   */
  removeVariable({dispatch}, variableId) {
    return new Promise((resolve, reject) => {
      variableApi.removeVariable(variableId)
        .then(response => {
          dispatch(
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT)
          ).then(resolve).catch(reject);
        })
        .catch(reject);
    });
  },
  fetchVariables({commit, state}, options) {
    options = options || {};
    return new Promise((resolve, reject) => {
      variableApi.fetchVariables(options)
        .then(response => {
          commit(mutationTypes.SET_VARIABLES, response.data.result);
          resolve();
        })
        .catch(reject)
    });
  },
}

const mutations = {
  setVariables(state, variables) {
    state.variables = variables;
  },
  setVariable(state, variable) {
    const id = variable.id;
    let recursiveIterator = function(varArray) {
      for (let i in varArray) {
        if (varArray[i].id === id) {
          Object.assign(varArray[i], variable);
        }
        if ((varArray[i].children || []) !== []) {
          recursiveIterator(varArray[i].children);
        }
      }
    }
    recursiveIterator(state.variables);
  },
  addVariable(state, variable) {
    if (variable.parent !== null && variable.parent !== undefined) {
      let parent_id = variable.parent.id;
      if (parent_id !== undefined) {
        let recursiveIterator = function(varArray) {
          for (let i in varArray) {
            if (varArray[i].id === parent_id) {
              varArray[i].children.push(variable);
              return true;
            }
            if ((varArray[i].children || []) !== []) {
              let added = recursiveIterator(varArray[i].children);
              if (added) {
                return true;
              }
            }
          }
          return false;
        }
        recursiveIterator(state.variables);
      }
    }
    state.variables.push(variable);
  },
  removeVariable(state, variableId) {
    state.variables = state.variables.filter(
      variable => removeVariable(variable, v => v.id === variableId)
    );
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
