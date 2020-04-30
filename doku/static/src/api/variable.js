import {axiosInstance as axios} from './index';

const VARIABLE_API = window.variableApi || '/api/v1/variable/';

export default {
  updateVariables(variables) {
    return axios.put(VARIABLE_API, variables);
  },
  createVariable(variable) {
    return axios.post(VARIABLE_API, variable);
  },
  removeVariable(variableId) {
    return axios.delete(`${VARIABLE_API}${variableId}/`);
  },
  fetchVariables(options) {
    return axios.get(VARIABLE_API, {params: options});
  }
}
