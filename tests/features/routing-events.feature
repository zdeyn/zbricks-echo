# tests/features/routing-events.feature
Feature: Custom event dispatcher between standard routes and 404
	There is a custom event dispatcher which sits between the standard routes and the 404 handler.
    This allows for clean insertion of our domain-specific logic without disturbing the Flask ecosystem

	Background:
		Given the event dispatcher is installed

        # Scenario: Requesting non-existent endpoint triggers event dispatcher
        #     When I request the "/non-existent" endpoint
        #     Then the event dispatcher is called
        
        # Scenario: Event dispatcher handles the request
        #     When the event dispatcher receives the request
        #     Then the event dispatcher will handle the request

        Scenario: Requesting non-existent endpoint with event dispatcher
            When I request the "/non-existent" endpoint
            Then I should get a "404" status code

        Scenario: Requesting handled endpoint with event dispatcher
            When I request the "/handled-by-event" endpoint
            Then I should get a "200" status code