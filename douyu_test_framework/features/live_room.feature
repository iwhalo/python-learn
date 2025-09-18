Feature: Douyu Live Room Interaction
  As a viewer
  I want to interact with live rooms
  So that I can enjoy streaming content

  Background:
    Given I am on the Douyu homepage
    When I enter a live room

  Scenario: View live room details
    Then I should see the room title
    And I should see the streamer information
    And the video player should be visible

  Scenario: Check viewer count
    Then I should see the viewer count
    And the viewer count should be a number

  Scenario: Navigate back from live room
    When I navigate back to homepage
    Then I should be on the Douyu homepage
