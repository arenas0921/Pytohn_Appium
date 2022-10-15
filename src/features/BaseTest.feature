# Created by User23 at 21/09/2022
Feature: Primer appium test
  # Enter feature description here

  Scenario: test Scenario
    Given Start application in default device
    Then Close application


  Scenario: test Scenario hardcoded
    Given Application start with device Pixel2
    When I set <YOURNAME> and <HERNAME> in LoveMain Page
        |YOURNAME   |HERNAME   |
        |Roland     |Nasly     |
    #Then I answer 10 questions in test
    Then answer all questions in test
    And wait 10 seconds
    Then Close application