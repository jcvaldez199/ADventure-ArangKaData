import axios from 'axios'
import { UrlBase } from '../config'

// Move these to a config file
const getUrl = UrlBase.concat("/auth/getadmin")
const removeUrl = UrlBase.concat("/auth/removeadmin")


export const getAdmin = () => {
  axios
    .get(getUrl, 
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
    .then((response) => {
      console.log(response.data.status);
      localStorage.clear();
      window.location.reload();
    })
    .catch(error => {
      console.error("error",error);
    });
};

export const removeAdmin = () => {
  axios
    .get(removeUrl, 
        { headers: 
          { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
    .then((response) => {
      console.log(response.data.status);
      localStorage.clear();
      window.location.reload();
    })
    .catch(error => {
      console.error("error",error);
    });
};

