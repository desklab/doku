import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from "vuex/dist/logger";

import document from './modules/document';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    document
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
});
