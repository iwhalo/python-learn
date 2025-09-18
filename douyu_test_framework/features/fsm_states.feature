Feature: FSM State Management
  As a test framework
  I want to track page states using FSM
  So that I can ensure valid navigation flows

  Background:
    Given the FSM is initialized

  Scenario: Navigate through valid states
    Given I am in INITIAL state
    When I transition to HOME state
    Then the current state should be HOME
    And the state history should include "INITIAL, HOME"

  Scenario: Search transition
    Given I am in HOME state
    When I transition to SEARCH_RESULTS state
    Then the current state should be SEARCH_RESULTS
    And the previous state should be HOME

  Scenario: Live room navigation flow
    Given I am in HOME state
    When I transition to LIVE_ROOM state
    Then the current state should be LIVE_ROOM
    When I transition back to HOME state
    Then the current state should be HOME

  Scenario: Invalid transition handling
    Given I am in LIVE_ROOM state
    When I attempt an invalid transition to LOGIN state
    Then the transition should fail
    And the current state should remain LIVE_ROOM
