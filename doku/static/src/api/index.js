import axios from 'axios';

const axiosInstance = axios.create({
  xsrfCookieName: 'csrf_token',
  xsrfHeaderName: 'X-CSRF-TOKEN'
});

export {
  axiosInstance
}