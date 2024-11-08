const axios = require('axios');

const render = 'quintoproyecto.onrender.com'; 

axios.get(`http://${render}`)
  .then(response => {
    console.log('Response data:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.message);
  });