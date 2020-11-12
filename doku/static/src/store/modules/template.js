import templateApi from '../../api/template';
import * as mutationTypes from '../types/mutations';
import * as actionTypes from '../types/actions';
import * as ns from '../namespace';

const state = {
  template: (window.templateObj !== undefined) ? JSON.parse(window.templateObj) : {},
  templates: (window.templates !== undefined) ? JSON.parse(window.templates) : {},
}

const getters = {}

const actions = {
  fetchTemplates({commit}, options) {
    return new Promise((resolve, reject) => {
      templateApi.fetchTemplates(options)
        .then((response) => {
          commit(mutationTypes.SET_TEMPLATES, response.data.result)
          resolve();
        })
        .catch(reject);
    });
  },
  updateTemplate({commit, rootState, dispatch}, template) {
    return new Promise((resolve, reject) => {
      templateApi.updateTemplate(template)
        .then(response => {
          let oldVariables = (rootState.variable.variables || []).map(v => v.name);
          commit(mutationTypes.SET_TEMPLATE, response.data);
          let hasMissing = response.data.available_fields.some(
            field => !oldVariables.includes(field)
          );
          if (hasMissing && rootState.document.document.id !== undefined) {
            let options = {
              document_id: rootState.document.document.id
            }
            dispatch(
              ns.document(actionTypes.FETCH_CURRENT_DOCUMENT),
              options, {root: true}
            ).then(resolve).catch(reject);
          } else {
            resolve();
          }
        })
        .catch(reject)
    });
  },
  removeTemplate({commit}, data){
    return new Promise((resolve, reject) => {
      templateApi.removeTemplate(data)
        .then(res => {
          commit(mutationTypes.REMOVE_TEMPLATE, res.data);
          resolve()
        }).catch(reject);
    });
  },
  addStylesheet({commit, dispatch, state}, data) {
    return new Promise((resolve, reject) => {
      if (!data.hasOwnProperty('url')) {
        throw Error('Missing url');
      }
      if (!data.hasOwnProperty('data')) {
        throw Error('Missing form data');
      }
      templateApi.addStylesheet(data.url, data.data)
        .then(res => {
          commit(mutationTypes.SET_TEMPLATE, res.data);
          commit(
            ns.stylesheet(mutationTypes.SET_STYLESHEETS),
            res.data.styles,
            {root: true}
          );
          resolve()
        }).catch(reject);
    });
  },
  removeStylesheet({commit, dispatch, state}, data) {
    return new Promise((resolve, reject) => {
      if (!data.hasOwnProperty('url')) {
        throw Error('Missing url');
      }
      if (!data.hasOwnProperty('data')) {
        throw Error('Missing form data');
      }
      templateApi.removeStylesheet(data.url, data.data)
        .then(res => {
          commit(mutationTypes.SET_TEMPLATE, res.data);
          commit(
            ns.stylesheet(mutationTypes.SET_STYLESHEETS),
            res.data.styles,
            {root: true}
          );
          resolve()
        }).catch(reject);
    });
  }
}

const mutations = {
  setTemplate(state, template) {
    Object.assign(state.template, template);
  },
  removeTemplate(state, template) {
    
  },
  setTemplates(state, templates) {
    state.templates = templates;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
