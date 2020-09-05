import {axiosInstance as axios} from './index';

const SNIPPET_API = window.snippetApi || '/api/v1/snippet/';

export default {
  fetchSnippets(options) {
    options = options || {};
    return axios.get(SNIPPET_API, options);
  }
}
