Feature: Recommendation Feed
  As a user
  I want to receive personalized recommendations
  So that I can discover new places

  Scenario: Get recommendation feed
    Given I am an authenticated user
    And I have checked into some places
    And recommendations have been generated
    When I request my recommendation feed
    Then I should receive personalized recommendations
    And the recommendations should be sorted by score
