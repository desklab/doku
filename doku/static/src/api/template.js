import {axiosInstance as axios} from './index';

const TEMPLATE_API = window.templateApi || '/api/v1/template/';

export default {
  updateTemplate(template) {
    return axios.put(TEMPLATE_API, template);
  },
}
