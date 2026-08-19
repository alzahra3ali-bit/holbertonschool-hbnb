document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');

    const addReviewSection = document.getElementById('add-review-button');
    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
        }
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const authenticatedToken = checkAuthentication();
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review').value;
            const ratingValue = document.getElementById('rating') ? document.getElementById('rating').value : null;

            await submitReview(authenticatedToken, placeId, reviewText, ratingValue);
        });
    }
});

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('place_id');
}

async function submitReview(token, placeId, reviewText, ratingValue) {
    try {
        const response = await fetch('YOUR_API_ENDPOINT_HERE', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: ratingValue
            })
        });

        handleResponse(response);
    } catch (error) {
        alert('An error occurred while submitting the review.');
    }
}

function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) reviewForm.reset();
    } else {
        alert('Failed to submit review');
    }
}
