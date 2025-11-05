Feature: Plan Management
  As a user
  I want to manage plans
  So that I can organize events

  Scenario: Create a new plan
    Given I am an authenticated user
    And there is a place available
    When I create a plan for that place
    Then the plan should be created successfully
    And the plan should have the correct details

  Scenario: Search for nearby plans
    Given there are multiple plans in different locations
    When I search for plans near a specific location
    Then I should receive only plans within the specified radius
