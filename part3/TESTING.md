# Part 2 Testing Documentation

This document summarizes the testing process, highlighting both successful cases and edge cases.

## What was tested

The following checks were added and verified:

- Swagger documentation endpoints are available
  - Swagger UI at `/docs`
  - OpenAPI spec at `/swagger.json`
- User registration flow was tested for both success and failure cases
  - Good scenario: a valid user payload returns HTTP 201 and creates the user
  - Bad scenario: an invalid email returns HTTP 400 with a JSON error message
- Error handling was improved for smoother client responses
  - Invalid input now returns a structured message such as `{"error": "Invalid email address"}` instead of exposing a server traceback

## Test command

Run the automated tests from the Part 2 folder with:

```bash
python -m unittest -v tests.test_swagger tests.test_api_endpoints
```

You can also verify the user registration behavior manually with the app running:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Ghaida","last_name":"alsabti","email":"alsabtighaida@gmail.com"}'
```

## Current result

The automated test run completed successfully with the following outcome:

- 4 tests ran
- 0 failures
- 0 errors

## Notes

The Swagger documentation is now exposed for the API, and the user creation endpoint now handles both successful and invalid requests more smoothly. The added unit tests cover both manual-style verification scenarios and automated regression checks.
