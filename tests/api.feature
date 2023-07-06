Feature: API Testing
  As a user
  I want to test the API endpoints
  So that I can ensure they work correctly

  Scenario: Query endpoint returns valid response
    Given the API is running
    When I make a GET request to "/endpoint?queryInput=tank"
    Then the response status code should be 200
    And the response body should contain valid JSON

  Scenario: Query endpoint returns sentiment scores
    Given the API is running
    When I make a GET request to "/endpoint"
    And the query input is "Prime Minister"
    Then the response status code should be 200
    And the response body should contain valid JSON
    And the response body should contain sentiment scores
