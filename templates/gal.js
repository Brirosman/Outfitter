const axios = require('axios');

const render = 'outfitter.onrender.com'; 

axios.get(`http://${render}`)
  .then(response => {
    console.log('Response data:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.message);
  });