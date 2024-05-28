# tests/features/events.feature
Feature: Custom event dispatcher
	There is a custom event dispatcher.
    Subscribers get notified when an event is dispatched that matches their subscription.

    Scenario Outline: "<event_type>" is dispatched
        Given a handler
        And the handler is subscribed to "<event_type>" events
        When I send "<event_type>" with its "<data_key>" property set to "<data_value>"
        Then the subscriber should receive "<event_type>" with its "<data_key>" property set to "<data_value>"

        Examples:
            | event_type     | data_key   | data_value |
            | zEvent         | data       | foo        |
            | zSampleEvent   | data       | bar        |
    
    Scenario: "zEvent" and "zSampleEvent" are both dispatched, received by single handler once
        Given a handler
        And the handler is subscribed to "zEvent" events
        And the handler is subscribed to "zSampleEvent" events
        When I send "zSampleEvent" with its "data" property set to "baz"
        Then the subscriber should receive "zSampleEvent" with its "data" property set to "baz"
        And the subscriber should not receive "zEvent"
