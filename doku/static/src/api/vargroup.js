import {axiosInstance as axios} from './index';

const VARIABLE_GROUP_API = window.vargroupApi || '/api/v1/vargroup/';

export default {
  createVariableGroup(variableGroup) {
    return axios.post(VARIABLE_GROUP_API, variableGroup);
  },
  removeVariableGroup(variableGroupId) {
    return axios.delete(`${VARIABLE_GROUP_API}${variableGroupId}/`);
  },
  updateVariableGroups(variableGroup) {
    return axios.patch(VARIABLE_GROUP_API, variableGroup);
  }
}
