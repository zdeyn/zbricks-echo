# tests/features/events.feature
Feature: Custom event dispatcher
	There is a custom event dispatcher.
    Subscribers get notified when an event is dispatched that matches their subscription.

    Scenario Outline: "<event_type>" is dispatched
        Given a handler
        And the handler is subscribed to "<event_type>" events
        When I send "<event_type>" with its "<data_key>" property set to "<data_value>"
        Then the handler should recieve "<event_type>" with its "<data_key>" property set to "<data_value>"

        Examples:
            | event_type     | data_key   | data_value |
            | zEvent         | data       | foo        |
            | zSampleEvent   | data       | bar        |
    
    Scenario: One handler, two subscriptions, "zSampleEvent" dispatched, only "zSampleEvent" recieved
        Given a handler
        And the handler is subscribed to "zEvent" events
        And the handler is subscribed to "zSampleEvent" events
        When I send "zSampleEvent" with its "data" property set to "baz"
        Then the handler should recieve "zSampleEvent" with its "data" property set to "baz"
        And the handler should not recieve "zEvent"
    
    Scenario: One handler, two subscriptions, "zEvent" dispatched, only "zEvent" recieved
        Given a handler
        And the handler is subscribed to "zEvent" events
        And the handler is subscribed to "zSampleEvent" events
        When I send "zEvent" with its "data" property set to "qux"
        Then the handler should recieve "zEvent" with its "data" property set to "qux"
        And the handler should not recieve "zSampleEvent"
    
    Scenario: Two handlers, "zSampleEvent" dispatched, both handlers recieve "zSampleEvent"
        Given a handler named "base" subscribed to "zEvent" events
        And a handler named "extended" subscribed to "zSampleEvent" events
        When I send "zEvent" with its "data" property set to "woot"
        Then the handler named "base" should recieve "zSampleEvent" with its "data" property set to "woot"
        And the handler named "extended" should recieve "zSampleEvent" with its "data" property set to "woot"

