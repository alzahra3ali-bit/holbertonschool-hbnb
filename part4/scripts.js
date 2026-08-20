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
  });