 document.addEventListener('DOMContentLoaded', () => { //wait till page fully loaded
      const loginForm = document.getElementById('login-form');

      if (loginForm) {
          loginForm.addEventListener('submit', async (event) => {
              event.preventDefault(); //to stop browser behaviour like reloading page

              const email = document.getElementById('email').value;
              const password = document.getElementById('password').value;
              
              try {
                await loginUser(email, password)
              }
              catch(err) {
                alert('Login failed: ' + err.message); 
              }
          });
      }

      async function loginUser(email, password) {
      const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
      });
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`; //store the token in a cookie
            window.location.href = 'index.html';
        } else {
      alert('Login failed: ' + response.statusText);
  }
  }

   function checkAuthentication() {
      const token = getCookie('token');
      const loginLink = document.getElementById('login-link');

      if (!token) {
          loginLink.style.display = 'block';
      } else {
          loginLink.style.display = 'none';
          // Fetch places data if the user is authenticated
          fetchPlaces(token);
      }
  }
  function getCookie(name) {
      // Function to get a cookie value by its name
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1); //skip equal sign
        }
      }
      return null;
  }

    async function fetchPlaces(token) {
      // Make a GET request to fetch places data
      const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}` // Include the token in the Authorization header
        }
        });

        if (!response.ok) {
			throw new Error('Error fetching places.');
		}

        const places = await response.json();
		displayPlaces(places); // Handle the response and pass the data to displayPlaces function
        
        function displayPlaces(places) {
            const placesList = document.getElementById('places-list');
            if (!placesList) {
                return;
            }

            placesList.innerHTML = ''; // Clear the current content of the places list
            
            // Iterate over the places data
            places.forEach(place => {
			const placeDiv = document.createElement('div'); // For each place, create a div element and set its content
			placeDiv.classList.add('place');
			placesList.appendChild(placeDiv); // Append the created element to the places list
			placeDiv.dataset.price = place.price;
		    });
            
            document.getElementById('price-filter').addEventListener('change', (event) => {
                // Get the selected price value
                const selectedPrice = parseFloat(event.target.value);

                // Iterate over the places and show/hide them based on the selected price
                const placeElements = document.querySelectorAll('.place');
                placeElements.forEach(place => {
                const placePrice = parseFloat(place.dataset.price);
                if (isNaN(selectedPrice) || placePrice <= selectedPrice) {
                    place.style.display = 'block';
                } else {
                    place.style.display = 'none';
                }
                });  
            });
  
        }
  }
  });