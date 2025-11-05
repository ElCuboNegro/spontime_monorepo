Feature: Place Recommendations
  As a user
  I want to receive personalized place recommendations
  So that I can discover new places to visit

  Scenario: View recommendation feed
    Given I am logged in
    And I have check-in history
    When I navigate to the recommendations page
    Then I should see a personalized feed of place recommendations
    And each recommendation should show:
      | name        |
      | category    |
      | score       |
      | distance    |
      | photo       |

  Scenario: Filter recommendations by category
    Given I am on the recommendations page
    When I select a category filter "restaurant"
    Then I should only see restaurant recommendations
    And the recommendations should be sorted by relevance

  Scenario: View recommendation details
    Given I am on the recommendations page
    When I click on a recommendation
    Then I should see detailed information about the place
    And I should see similar places
    And I should see user reviews if available

  Scenario: Save a recommendation
    Given I am viewing a recommendation
    When I click "Save for later"
    Then the recommendation should be added to my saved list
    And I should receive a confirmation

  Scenario: Dismiss a recommendation
    Given I am viewing a recommendation
    When I click "Not interested"
    Then the recommendation should be hidden
    And future recommendations should be adjusted

  Scenario: Create a plan from recommendation
    Given I am viewing a recommendation
    When I click "Create Plan"
    Then I should be redirected to the plan creation form
    And the place should be pre-filled
    And I can add additional details

  Scenario: Share a recommendation
    Given I am viewing a recommendation
    When I click "Share"
    And I select friends to share with
    Then they should receive a notification
    And they should be able to view the recommendation
