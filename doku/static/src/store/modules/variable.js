import variableApi from '../../api/variable';
import * as actionTypes from '../types/actions';
import * as ns from '../namespace';

const state = {};

const getters = {};

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
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT),
            null, { root: true }
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
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT),
            null, { root: true }
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
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT),
            null, { root: true }
          ).then(resolve).catch(reject);
        })
        .catch(reject);
    });
  },
};

const mutations = {};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
