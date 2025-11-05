Feature: Plan Management
  As a user
  I want to create and manage plans
  So that I can organize activities with friends

  Scenario: Create a new plan
    Given I am logged in
    And I am on the plans page
    When I click "Create New Plan"
    And I fill in the plan details:
      | title           | Picnic in the Park        |
      | description     | Let's have a picnic!      |
      | scheduled_time  | 2024-12-25T14:00:00Z     |
      | place           | Central Park              |
    And I submit the plan form
    Then the plan should be created
    And I should see the plan in my plans list

  Scenario: View plan details
    Given I am logged in
    And I have existing plans
    When I click on a plan
    Then I should see the plan details
    And I should see the location on a map
    And I should see the list of participants

  Scenario: Update a plan
    Given I am logged in
    And I am the creator of a plan
    When I click "Edit Plan"
    And I update the plan details
    And I save the changes
    Then the plan should be updated
    And I should see the updated information

  Scenario: Delete a plan
    Given I am logged in
    And I am the creator of a plan
    When I click "Delete Plan"
    And I confirm the deletion
    Then the plan should be removed
    And I should no longer see it in my plans list

  Scenario: Search nearby plans
    Given I am logged in
    And I am on the plans page
    When I enable location services
    And I search for plans nearby
    Then I should see a list of plans near my location
    And each plan should show the distance from my location

  Scenario: Join a plan
    Given I am logged in
    And I see a public plan
    When I click "Join Plan"
    Then I should be added as a participant
    And I should receive a confirmation

  Scenario: Leave a plan
    Given I am logged in
    And I am a participant in a plan
    When I click "Leave Plan"
    And I confirm my decision
    Then I should be removed from the participants
    And the plan creator should be notified
