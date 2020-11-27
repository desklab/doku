import stylesheetApi from '../../api/stylesheet';
import * as mutationTypes from '../types/mutations';
import * as actionTypes from '../types/actions';

const state = {
  stylesheets: (window.stylesheets !== undefined) ? JSON.parse(window.stylesheets) : [],
};

const getters = {};

const actions = {
  uploadStylesheet({commit, state}, data) {
    return new Promise((resolve, reject) => {
      if (!data.hasOwnProperty('url')) {
        throw Error('Missing url');
      }
      if (!data.hasOwnProperty('formData')) {
        throw Error('Missing form data');
      }
      stylesheetApi.uploadStylesheet(data.url, data.formData)
        .then(response => {
          commit(mutationTypes.SET_STYLESHEET, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  updateStylesheet({commit, state, dispatch}, data) {
    return new Promise((resolve, reject) => {
      stylesheetApi.updateStylesheets(data)
        .then(response => {
          commit(mutationTypes.SET_STYLESHEET, response.data);
          resolve();
        })
        .catch(reject);
    });
  },
  fetchStylesheets({commit, state}, options) {
    options = options || {};
    return new Promise((resolve, reject) => {
      stylesheetApi.fetchStylesheets(options)
        .then(response => {
          commit(mutationTypes.SET_STYLESHEETS, response.data.results);
          resolve();
        })
        .catch(reject);
    });
  },
  deleteStylesheet({commit, dispatch, state}, data) {
    return new Promise((resolve, reject) => {
      if (!data.hasOwnProperty('url')) {
        throw Error('Missing url');
      }
      if (!data.hasOwnProperty('id')) {
        throw Error('Missing id');
      }
      stylesheetApi.deleteStylesheet(data.url)
        .then(res => {
          commit(mutationTypes.DELETE_STYLESHEET, data.id);
          resolve();
        }).catch(reject);
    });
  },
  setStylesheets({commit, state}, data){
    return new Promise((resolve, reject) => {
      stylesheetApi.setStylesheets(data)
        .then(res => {
          commit(mutationTypes.SET_STYLESHEETS, data);
          resolve();
        }).catch(reject);
    });
  },
};

const mutations = {
  setStylesheets(state, styles) {
    state.stylesheets = styles;
  },
  setStylesheet(state, stylesheet) {
    const id = stylesheet.id;
    for (let i in state.stylesheets) {
      if (state.stylesheets[i].id === id) {
        Object.assign(state.stylesheets[i], stylesheet);
        return;
      }
    }
  },
  deleteStylesheet(state, id) {
    for (var i = 0; i < state.stylesheets.length; i++) {
      if (state.stylesheets[i].id == id){
        state.stylesheets.splice(i, 1);
        break;
      }
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
