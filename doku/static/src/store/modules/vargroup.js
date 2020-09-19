import vargroupApi from '../../api/vargroup';
import * as actionTypes from '../types/actions';
import * as ns from '../namespace';

const state = {}

const getters = {}

const actions = {
  /**
   * Create Variable Group for Document
   *
   * Creates a new variable group based on the supplied parameter.
   *
   * Instead of using mutations, the state is handled by the document
   * store. It is updated by calling `fetchCurrentDocument`.
   *
   * @param dispatch - Supplied by Vuex (used to dispatch Document action)
   * @param vargroup - Objects that describe the new variable group
   * @returns {Promise<void>}
   */
  createVariableGroup({dispatch}, vargroup) {
    return new Promise((resolve, reject) => {
      vargroupApi.createVariableGroup(vargroup)
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
   * Remove Variable Group
   *
   * This will remove a variable group (i.e. delete) from the document.
   * It will no longer be accessible, however, all its variables will be
   * appended to the document root.
   *
   * Instead of using mutations, the state is handled by the document
   * store. It is updated by calling `fetchCurrentDocument`.
   *
   * @param dispatch - Supplied by Vuex (used to dispatch Document action)
   * @param variableGroupId - ID for the variable group to be deleted
   * @returns {Promise<void>}
   */
  removeVariableGroup({dispatch}, variableGroupId) {
    return new Promise((resolve, reject) => {
      vargroupApi.removeVariableGroup(variableGroupId)
        .then(response => {
          dispatch(
            ns.document(actionTypes.FETCH_CURRENT_DOCUMENT),
            null, { root: true }
          ).then(resolve).catch(reject);
        })
        .catch(reject);
    });
  },
}

const mutations = {}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
