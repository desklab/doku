import {axiosInstance as axios} from './index';

const STYLESHEET_API = window.stylesheetApi || '/api/v1/stylesheet/';

export default {
  updateStylesheets(stylesheets) {
    return axios.put(STYLESHEET_API, stylesheets);
  },
  fetchStylesheets(options) {
    options = options || {};
    return axios.get(STYLESHEET_API, options);
  },
  uploadStylesheet(url, formData) {
    return axios.put(url,
      formData, {
        headers: {'Content-Type': 'multipart/form-data'}
      });
  },
  createStylesheet(stylesheet) {
    return axios.post(STYLESHEET_API, stylesheet);
  },
  deleteStylesheet(stylesheetURL) {
    return axios.delete(stylesheetURL);
  }
}
