Feature: Douyu Homepage Navigation
  As a user of Douyu platform
  I want to navigate the homepage
  So that I can access different sections of the website

  Background:
    Given I am on the Douyu homepage

  Scenario: Access Douyu homepage successfully
    Then I should see the Douyu logo
    And the page title should contain "斗鱼"

  Scenario: Search for content
    When I search for "英雄联盟"
    Then I should see search results
    And the search results should be displayed

  Scenario: Navigate to game category
    When I click on a category from navigation
    Then I should be on the category page
    And I should see live room listings

  Scenario: Enter a live room
    When I click on the first live room
    Then I should be on a live room page
    And I should see the video player
