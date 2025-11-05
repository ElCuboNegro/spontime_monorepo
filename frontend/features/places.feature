Feature: Place Discovery
  As a user
  I want to discover and interact with places
  So that I can explore new locations

  Scenario: Browse places
    Given I am logged in
    And I am on the places page
    Then I should see a list of places
    And each place should display:
      | name        |
      | category    |
      | address     |
      | rating      |
      | photo       |

  Scenario: Search for places
    Given I am on the places page
    When I enter "coffee shop" in the search bar
    And I submit the search
    Then I should see places matching "coffee shop"
    And the results should be sorted by relevance

  Scenario: Filter places by category
    Given I am on the places page
    When I select category "restaurant"
    Then I should only see restaurants
    And I can apply additional filters

  Scenario: View place on map
    Given I am viewing places
    When I click "Map View"
    Then I should see places displayed on a map
    And I can click markers to see place details

  Scenario: Check in to a place
    Given I am logged in
    And I am at a place location
    When I click "Check In"
    And I confirm my check-in
    Then my check-in should be recorded
    And my friends should be notified if I choose to share

  Scenario: View check-in history
    Given I am logged in
    When I navigate to my profile
    And I click "Check-in History"
    Then I should see all my past check-ins
    And each check-in should show:
      | place       |
      | date        |
      | time        |
      | notes       |

  Scenario: Add a new place
    Given I am logged in
    When I click "Add Place"
    And I fill in the place details:
      | name        | New Coffee Shop           |
      | category    | coffee                    |
      | address     | 123 Main St, New York, NY |
      | latitude    | 40.7128                   |
      | longitude   | -74.0060                  |
    And I submit the form
    Then the place should be created
    And I should see it in the places list
