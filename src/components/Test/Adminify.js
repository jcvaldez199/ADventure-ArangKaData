import axios from 'axios'

// Move these to a config file
const getUrl = "http://localhost:3000/auth/getadmin"
const removeUrl = "http://localhost:3000/auth/removeadmin"


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

