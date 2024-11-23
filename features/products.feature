Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product" in the title
    And I should not see "404 Not Found"


Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Description" to "Unknown"
    And I select "True" in the "Available" dropdown
    And I set the "Price" to "3.75"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Happy" in the "Name" field
    And I should see "Unknown" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "3.75" in the "Price" field    