# tests/features/routing-exceptions.feature
Feature: Handling of routing exceptions
	Accessing a non-existent endpoint should return a 404 status code

	Scenario: Requesting non-existent endpoint
		When I request the "/non-existent" endpoint
		Then I should get a "404" status code
