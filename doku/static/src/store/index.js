import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';

import document from './modules/document';
import template from './modules/template';
import variable from './modules/variable';
import vargroup from './modules/vargroup';
import stylesheet from './modules/stylesheet';
import resource from './modules/resource';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  modules: {
    document,
    template,
    variable,
    stylesheet,
    resource,
    vargroup
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
});
