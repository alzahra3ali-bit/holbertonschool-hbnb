document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = 'http://localhost:5000/api/v1';
    const token = getCookie('token');

    const addReviewSection = document.getElementById('add-review-button');
    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
        }
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

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
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                await loginUser(email, password);
            } catch (err) {
                alert('Login failed: ' + err.message);
            }
        });
    }
});

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
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        alert('Login failed: ' + response.statusText);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function initPlaceDetailsPage() {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    
    if (!placeId) {
        document.getElementById('place-details').innerHTML = 
            '<p>Error: No place ID provided in URL.</p>';
        return;
    }
    
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display = 'block';
            const link = addReviewSection.querySelector('a');
            if (link) {
                link.href = `add_review.html?id=${placeId}`;
            }
        } else {
            addReviewSection.style.display = 'none';
        }
    }
    
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'inline-block';
    }
    
    await fetchPlaceDetails(placeId, token);
    await fetchPlaceReviews(placeId, token);
}

async function fetchPlaceDetails(placeId, token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    
    try {
        const response = await fetch(`${API_BASE}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });
        
        if (!response.ok) {
            throw new Error(`Failed to load place. Status: ${response.status}`);
        }
        
        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('place-details').innerHTML = 
            `<p>Sorry, we couldn't load this place.</p>`;
    }
}

async function fetchPlaceReviews(placeId, token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    
    try {
        const response = await fetch(`${API_BASE}/places/${placeId}/reviews/`, {
            method: 'GET',
            headers: headers
        });
        
        if (!response.ok) {
            displayReviews([]);
            return;
        }
        
        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error('Error loading reviews:', error);
        displayReviews([]);
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    
    section.innerHTML = `
        <div class="place-info">
            <h1>${place.title || 'Unknown Place'}</h1>
            <p><strong>Price per night:</strong> $${place.price}</p>
            <p><strong>Description:</strong> ${place.description || 'No description'}</p>
            <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
        </div>
    `;
}

function displayReviews(reviews) {
    const section = document.getElementById('reviews');
    section.innerHTML = '<h2>Reviews</h2>';
    
    if (!reviews || reviews.length === 0) {
        const noReviews = document.createElement('p');
        noReviews.textContent = 'No reviews yet. Be the first to review!';
        section.appendChild(noReviews);
        return;
    }
    
    reviews.forEach(review => {
        const card = document.createElement('article');
        card.className = 'review-card';
        card.innerHTML = `
            <p>${review.text}</p>
            <p><strong>Rating:</strong> ${review.rating}/5</p>
        `;
        section.appendChild(card);
    });
}

function initAddReviewPage() {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
    
    if (!placeId) {
        alert('No place selected.');
        window.location.href = 'index.html';
        return;
    }
    
    displayPlaceName(placeId, token);
    
    const form = document.getElementById('review-form');
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            
            await submitReview(placeId, reviewText, rating, token);
        });
    }
}

async function displayPlaceName(placeId, token) {
    try {
        const response = await fetch(`${API_BASE}/places/${placeId}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const place = await response.json();
            const el = document.getElementById('place-name');
            if (el) {
                el.innerHTML = `<strong>${place.title}</strong>`;
            }
        }
    } catch (error) {
        console.error('Could not load place name:', error);
    }
}

async function submitReview(placeId, reviewText, rating, token) {
    try {
        const response = await fetch(`${API_BASE}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId
            })
        });
        
        if (response.ok) {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert(`Failed to submit review: ${errorData.error || 'Please try again'}`);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Network error. Please try again.');
    }
}
});