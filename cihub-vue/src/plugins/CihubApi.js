import axios from 'axios'

const CihubApi = {}
/* eslint-disable */
CihubApi.install = function(Vue) {
  const axiosInstance = axios.create({
    baseURL: `${window.location.protocol}//${window.location.host}/api/`
  });
  const backend = {};
  backend.loggedIn = false;

  backend.authenticate = function (usernameAuth, passwordAuth) {

    return axiosInstance.get('cc.json', {
      auth: {
        username: usernameAuth,
        password: passwordAuth
      }
    });
  };

  backend.getUrl = function(url) {
    return axiosInstance.get(url)
  };

  Vue.prototype.$backend = backend;
  Vue.prototype.$getBuilds = function() {
    return backend.getUrl(`cc.json`)
  };
  Vue.prototype.$http = axiosInstance;
}

export default CihubApi;