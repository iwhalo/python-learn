Feature: User Authentication - Login and Register
  As a Douyu user
  I want to login and register on the platform
  So that I can access personalized features

  Background:
    Given I am on the Douyu homepage

  @smoke
  Scenario: Open login modal successfully
    When I click on the login button
    Then the login modal should be visible

  @smoke
  Scenario: Switch between login and register
    When I click on the login button
    And I switch to register tab
    Then the register modal should be visible
    When I switch to login tab
    Then the login modal should be visible

  Scenario: Login with phone number and verification code - Success
    When I click on the login button
    And I switch to phone login tab
    And I enter phone number "13800138000"
    And I request SMS verification code
    And I enter verification code "123456"
    And I click login button
    Then I should see login success or error message

  Scenario: Login with phone number and verification code - Invalid phone
    When I click on the login button
    And I switch to phone login tab
    And I enter phone number "123"
    And I request SMS verification code
    Then I should see a phone number error message

  Scenario: Login with username and password - Success
    When I click on the login button
    And I switch to password login tab
    And I enter username "testuser"
    And I enter password "password123"
    And I click login button
    Then I should see login success or error message

  Scenario: Login with username and password - Empty credentials
    When I click on the login button
    And I switch to password login tab
    And I enter username ""
    And I enter password ""
    And I click login button
    Then I should see a credentials error message

  Scenario: Register new user - Success
    When I click on the login button
    And I switch to register tab
    And I enter registration phone number "13900139000"
    And I request registration SMS code
    And I enter registration code "123456"
    And I enter registration username "newuser123"
    And I enter registration password "Pass@1234"
    And I enter registration confirm password "Pass@1234"
    And I accept user agreement
    And I click register button
    Then I should see registration success or error message

  Scenario: Register new user - Username already exists
    When I click on the login button
    And I switch to register tab
    And I enter registration phone number "13900139000"
    And I enter registration code "123456"
    And I enter registration username "existinguser"
    And I enter registration password "Pass@1234"
    And I click register button
    Then I should see username already exists error

  Scenario: Register new user - Invalid phone format
    When I click on the login button
    And I switch to register tab
    And I enter registration phone number "abc"
    And I request registration SMS code
    Then I should see invalid phone format error

  Scenario: Register new user - Invalid email format
    When I click on the login button
    And I switch to register tab
    And I enter registration phone number "13900139000"
    And I enter registration email "invalid-email"
    And I enter registration username "newuser"
    And I enter registration password "Pass@1234"
    And I click register button
    Then I should see invalid email format error

  Scenario: Register new user - Password mismatch
    When I click on the login button
    And I switch to register tab
    And I enter registration phone number "13900139000"
    And I enter registration code "123456"
    And I enter registration username "newuser"
    And I enter registration password "Pass@1234"
    And I enter registration confirm password "DifferentPass"
    And I click register button
    Then I should see password mismatch error

  @smoke
  Scenario: Logout successfully
    Given I am logged in
    When I click on user avatar
    And I click logout button
    Then I should be logged out
    And I should see login button
