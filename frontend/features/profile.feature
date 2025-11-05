Feature: User Profile
  As a user
  I want to manage my profile
  So that I can personalize my experience and connect with friends

  Scenario: View my profile
    Given I am logged in
    When I navigate to my profile page
    Then I should see my profile information:
      | username        |
      | email           |
      | bio             |
      | location        |
      | profile picture |
      | interests       |

  Scenario: Edit profile information
    Given I am on my profile page
    When I click "Edit Profile"
    And I update my information:
      | bio       | Love exploring new places!  |
      | location  | New York, NY                |
    And I save the changes
    Then my profile should be updated
    And I should see the updated information

  Scenario: Upload profile picture
    Given I am editing my profile
    When I click "Change Photo"
    And I upload a new profile picture
    And I save the changes
    Then my profile picture should be updated
    And it should be visible on my profile

  Scenario: Set interests and preferences
    Given I am on my profile settings
    When I select my interests:
      | restaurants  |
      | coffee shops |
      | parks        |
      | museums      |
    And I save my preferences
    Then my recommendations should be personalized based on these interests

  Scenario: View activity statistics
    Given I am on my profile page
    When I view my statistics
    Then I should see:
      | total check-ins    |
      | places visited     |
      | plans created      |
      | plans attended     |
      | favorite category  |

  Scenario: Manage privacy settings
    Given I am on my profile settings
    When I adjust my privacy settings:
      | check-ins visible | Friends only |
      | profile visible   | Public       |
    And I save the settings
    Then my privacy preferences should be applied

  Scenario: View friend list
    Given I am on my profile page
    When I click "Friends"
    Then I should see my friends list
    And I can view their profiles
    And I can see their recent activity

  Scenario: Search for friends
    Given I am on the friends page
    When I search for "john"
    Then I should see users matching "john"
    And I can send friend requests

  Scenario: Delete account
    Given I am on my profile settings
    When I click "Delete Account"
    And I confirm the deletion
    And I enter my password
    Then my account should be permanently deleted
    And all my data should be removed
