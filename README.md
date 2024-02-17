# Authentic Food Reviews Based on Google Map

## Problem Statement:

#### 1) Difficult to identify whether the restaurants has halal certificate provided by JAKIM or not when searched in Google Map. (Searching "Halal Food" for example, will find the restaurants with the keyword "halal" in the reviews, therefore non-halal results will still appear)

#### 2) When you are deciding where to eat when you are hungry, typically you will judge the restaruarnts whether nice to eat or not based on their ratings and food reviews. After eating them, you will feel like overrated or scammed because the food isn't delicious at all.

## Solution:

#### Using Selenium/Google APIs to extract the food reviews, find out which restaurants has halal certification by JAKIM, which of them have their sources from HALAL vendors, and which reviews are boosted with fake accounts to get good ratings or intentionally trying to make the restaurants rating lower.

#### Look up at www.halal.gov.my or www.verifyhalal.com

## Scope of Location:

### Should I focus on areas which have:

#### 1) less malay populations and less obvious malay shops? 5 votes
#### or 
#### 2) more malay populations and more malay shops? 1 vote

## Git Commands

#### 1. ```git checkout -b your-branch-name```
#### 2. ```git add .``` or the specific file you want to add e.g. tests.py
#### 3. ```git commit -m "add your specific commit message here"```
#### 4. ```git push --set-upstream origin your-branch-name```

## Semantic Commit Messages

#### ```feat```: (new feature for the user, not a new feature for build script)
#### ```fix```: (bug fix for the user, not a fix to a build script)
#### ```docs```: (changes to the documentation)
#### ```style```: (formatting, missing semi colons, etc; no production code change)
#### ```refactor```: (refactoring production code, eg. renaming a variable)
#### ```test```: (adding missing tests, refactoring tests; no production code change)
#### ```chore```: (updating grunt tasks etc; no production code change)