Feature: User Authentication
  As a user
  I want to authenticate with the system
  So that I can access personalized features

  Scenario: User registration
    Given I am on the registration page
    When I fill in my registration details
    And I submit the registration form
    Then I should receive a confirmation message
    And my account should be created

  Scenario: User login
    Given I have a registered account
    When I enter my valid credentials
    And I submit the login form
    Then I should be logged in
    And I should see my dashboard

  Scenario: User logout
    Given I am logged in
    When I click the logout button
    Then I should be logged out
    And I should be redirected to the home page

  Scenario: Failed login attempt
    Given I am on the login page
    When I enter invalid credentials
    And I submit the login form
    Then I should see an error message
    And I should remain on the login page
