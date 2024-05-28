# tests/features/auth/auth-routes.feature
Feature: Auth system provides routes

	Scenario: Login Page returns redirect status code
		When I request the "/auth/login" endpoint
		Then I should get a "302" status code
		And I should see "discord.com/api/oauth2/authorize" in the "Location" field of the response headers