# tests/bdd/features/system/system-response.feature

Feature: System Response

  Scenario: System responds with Response object
    Given a system
    And a client
    When the client makes a request
    Then the system responds with a Response object
  
  Scenario: System responds with 404 Not Found
    Given a system
    And a client
    When a request is made for a non-existent resource
    Then the system responds with 404 Not Found
  
  Scenario: System responds with 200 OK
    Given a system with a resource
    And a client
    When a request is made for that resource
    Then the system responds with 200 OK
  
  Scenario: System responds with 500 Internal Server Error
    Given a system with a bugged resource
    And a client
    When a request is made for that resource
    Then the system responds with 500 Internal Server Error