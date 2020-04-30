import variableApi from '../../api/variable';
import * as mutationTypes from '../types/mutations';

const state = {
  variables: (window.variables !== undefined) ? JSON.parse(window.variables) : [],
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
  updateVariables({commit, state}, variables) {
    return new Promise((resolve, reject) => {
      variableApi.updateVariables(variables)
        .then(response => {
          commit(mutationTypes.SET_VARIABLES, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  updateVariable({commit, state}, variable) {
    return new Promise((resolve, reject) => {
      variableApi.createVariable(variable)
        .then(response => {
          commit(mutationTypes.SET_VARIABLE, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  createVariable({commit, state}, variable) {
    return new Promise((resolve, reject) => {
      variableApi.createVariable(variable)
        .then(response => {
          commit(mutationTypes.ADD_VARIABLE, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  removeVariable({commit, state}, variableId) {
    return new Promise((resolve, reject) => {
      variableApi.removeVariable(variableId)
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
      variableApi.fetchVariables(options)
        .then(response => {
          commit(mutationTypes.SET_VARIABLES, response.data);
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
