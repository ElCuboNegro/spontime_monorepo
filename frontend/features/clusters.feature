Feature: Place Clusters
  As a user
  I want to view clustered places
  So that I can discover areas with multiple interesting locations

  Scenario: View place clusters on map
    Given I am logged in
    And I am on the explore page
    When I view the map
    Then I should see clusters of nearby places
    And each cluster should show the number of places

  Scenario: Zoom into a cluster
    Given I am viewing clusters on the map
    When I click on a cluster
    Then the map should zoom in
    And I should see the individual places within that cluster

  Scenario: Filter clusters by category
    Given I am viewing clusters
    When I select category filter "restaurant"
    Then clusters should only show restaurant places
    And the cluster sizes should update accordingly

  Scenario: View cluster details
    Given I am viewing a cluster
    When I click on cluster information
    Then I should see:
      | total places    |
      | radius          |
      | center location |
      | categories      |

  Scenario: Create plan for cluster area
    Given I am viewing a cluster
    When I click "Plan event here"
    Then I should see the plan creation form
    And the location should be set to the cluster center
    And I should see suggestions from places in the cluster
