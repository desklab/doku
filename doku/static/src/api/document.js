import {axiosInstance as axios} from './index';

const DOCUMENT_API = window.documentApi || '/api/v1/document/';
const VARIABLE_API = window.variableApi || '/api/v1/variable/';

export default {
  updateDocument(document) {
    return axios.put(DOCUMENT_API, document);
  },
  createDocument(document) {
    return axios.post(DOCUMENT_API, document);
  },
  updateVariables(variables) {
    return axios.put(VARIABLE_API, variables);
  },
  removeVariable(variableId) {
    return axios.delete(`${VARIABLE_API}${variableId}/`);
  },
  fetchVariables(options) {
    return axios.get(VARIABLE_API, {params: options});
  }
}
