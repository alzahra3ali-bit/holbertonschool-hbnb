const API_BASE = 'http://localhost:5000/api/v1';

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) return value;
    }
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

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('place-details')) {
        initPlaceDetailsPage();
    }
    else if (document.getElementById('review-form')) {
        initAddReviewPage();
    }
});