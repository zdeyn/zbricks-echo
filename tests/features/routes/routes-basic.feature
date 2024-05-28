# tests/features/routing-basic.feature
Feature: Can define routes for the application
	Basic routing capabilities

	Background:
		Given the endpoint "/hello" exists

	Scenario: Requesting /hello gives correct text
		When I request the "/hello" endpoint
		Then I should see "Hello, World!"

	Scenario: Requesting /hello gives correct status
		When I request the "/hello" endpoint
		Then I should get a "200" status code