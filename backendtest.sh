#!/bin/bash

echo "Creating a new user..."
curl -X POST -H "Content-Type: application/json" -d '{"username": "burhansecretuser3", "email": "testuser5@example.com", "password": "asdasd"}' localhost:5000/api/flashcards/register



# echo "Generating access token for the user..."
# TOKEN=$(curl -X POST -H "Content-Type: application/json" -d '{"username": "burhansecretuser", "password": "asdasd"}' localhost:5000/api/flashcards/login | jq -r .access_token)

# echo "Token is: $TOKEN"


# echo "Fetching all flashcards..."
# curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" https://flashcardapp-be-uhrgp63gla-uc.a.run.app/api/flashcards/

# echo "Updating a flashcard..."
# curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"word": "GANGEDITED", "definition": "testdefinition_updated"}' http://127.0.0.1:5000/api/flashcards/4

# echo "Deleting a flashcard..."
# curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/api/flashcards/5



#!/bin/bash

# Test POST endpoint to create a new flashcard
# echo "Testing POST /api/flashcards"
# curl -X POST -H "Content-Type: application/json" -d '{"word": "ganggang", "definition": "stupid slang"}' http://127.0.0.1:5000/api/flashcards/
# echo "\n"

# Test GET endpoint to fetch all flashcards
# echo "Testing GET /api/flashcards"
# curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/api/flashcards/
# echo "\n"

# # # Assume we have a flashcard with id=1 for the following tests
# flashcard_id=2

# # # Test GET endpoint to fetch a single flashcard
# echo "Testing GET /flashcards/${flashcard_id}"
# curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/api/flashcards/${flashcard_id}
# echo "\n"

# # Test PUT endpoint to update a flashcard
# echo "Testing PUT /flashcards/${flashcard_id}"
# curl -X PUT -H "Content-Type: application/json" -d '{"word": "serendipity222", "definition": "NEW DEF Finding something good without looking for it."}' http://127.0.0.1:5000/api/flashcards/${flashcard_id}
# echo "\n"

# # Test DELETE endpoint to delete a flashcard
# echo "Testing DELETE /flashcards/${flashcard_id}"
# curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:5000/api/flashcards/${flashcard_id}
# echo "\n"
