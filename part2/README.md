# Holberton HBNB - Part 2

This directory contains the Part 2 portion of the Holberton HBNB project. Below is a brief description of the top-level files and subdirectories.

- `part1/`: Previous project work for Part 1 (contains its own README).

- `config.py`: Project configuration settings (environment flags, constants).
- `requirements.txt`: Python dependencies required to run the app.
- `run.py`: Small runner script to start the application for development/testing.

- `Install dependencies`: Run `pip install -r requirements.txt` to install required packages.

- `app/`: Main application package.
	- `api/`: REST API endpoints organized by version (`v1/`) — contains route handlers for amenities, places, reviews, and users.
	- `models/`: Domain models for the app (e.g., `amenity.py`, `place.py`, `review.py`, `user.py`).
	- `persistence/`: Repository and persistence-related code (data access and storage abstractions).
	- `services/`: Business-logic layer and facade helpers used by the API and CLI.

Use this README as a quick map to the project structure; open the files inside each folder for implementation details.

Swagger documentation is now available through the Flask-RESTX UI.

- Open http://127.0.0.1:5000/docs to view the interactive Swagger documentation.
- The OpenAPI spec is available at http://127.0.0.1:5000/swagger.json.
- Run the app with: python run.py

For testing details, including the automated Swagger and API endpoint checks, see [TESTING.md](TESTING.md).

