import {axiosInstance as axios} from './index';

const DOCUMENT_API = window.documentApi || '/api/v1/document/';

export default {
  updateDocument(document) {
    return axios.put(DOCUMENT_API, document);
  },
  createDocument(document) {
    return axios.post(DOCUMENT_API, document);
  },
  removeDocument(documentId) {
    return axios.delete(`${DOCUMENT_API}${documentId}/`);
  },
  fetchDocuments(options) {
    options = options || {};
    return axios.get(DOCUMENT_API, options);
  },
  bulkDownload(include = [], exclude = [], all = false) {
    let data = {include, exclude, all};
    return axios.post(`${DOCUMENT_API}download/request`, data);
  },
  fetchIDs() {
    return axios.get(`${DOCUMENT_API}ids`);
  }
}
