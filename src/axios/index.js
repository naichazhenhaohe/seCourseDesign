import axios from 'axios';

const myUrl = 'http://111.230.206.17:8080';

axios.defaults.baseURL = myUrl;
axios.create({ 
  baseURL: myUrl+'/demo',
  timeout: 5000
});

export default axios;