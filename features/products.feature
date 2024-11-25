Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products


Background:
    Given the following products
        | name    | description        | price | available | image_url  |
        | Pen     | Blue ink pen       | 1.20  | True      |            |
        | Notebook| Spiral notebook    | 2.50  | False     |            |       
        | fluffy  | lion               | 0.99  | True      |            |
        | Mug     | Ceramic coffee mug | 5.00  | True      |            |


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


Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "fluffy"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fluffy" in the "Name" field
    And I should see "lion" in the "Description" field
    When I change "Description" to "kitty"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "kitty" in the "Description" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "kitty" in the results
    And I should not see "lion" in the results    


Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Mug" in the results
    And I should see "Pen" in the results
    And I should not see "Notebook" in the results    

Scenario: Read a Product
    Given I visit the "Home Page"
    And I set the "Id" to "1"
    When I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Pen" in the "Name" field
    And I should see "Blue ink pen" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "1.20" in the "Price" field

Scenario: Query products by name
    When I visit the "Home Page"
    And I set the "Name" to "Pen"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Pen" in the results
    And I should not see "Notebook" in the results
    And I should not see "fluffy" in the results
    And I should not see "Mug" in the results

Scenario: Query products by availability
    When I visit the "Home Page"
    And I select "False" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Notebook" in the results
    And I should not see "Pen" in the results
    And I should not see "fluffy" in the results
    And I should not see "Mug" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Pen"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Pen" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "product has been Deleted!"
    When I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Pen" in the results
