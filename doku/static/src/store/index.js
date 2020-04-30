import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from "vuex/dist/logger";

import document from './modules/document';
import template from './modules/template';
import variable from './modules/variable';
import stylesheet from './modules/stylesheet';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    document,
    template,
    variable,
    stylesheet
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
});
