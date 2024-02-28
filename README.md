# Jom Makan! : NLP categorization based on google map reviews

#### Visit the official website of Jom Makan! App >>>[HERE](https://jom-makan.onrender.com/)<<<

## Problem Statement:

#### 1) Difficult to identify whether the restaurants has halal certificate provided by JAKIM or not when searched in Google Map. (Searching "Halal Food" for example, will find the restaurants with the keyword "halal" in the reviews, therefore non-halal results will still appear)

#### 2) When you are deciding where to eat when you are hungry, typically you will judge the restaruarnts whether nice to eat or not based on their ratings and food reviews. However, you will find it tough and tedious to find the recommended dishes or food to avoid as you have to scan through the reviews 1 by 1.

#### 3) Sometimes, after your visit to the restaurant, you will feel like overrated or scammed because the food isn't delicious at all as per the review. You suspect that there are fake or paid reviews to increase the ratings of the restaurant.

#### 4) Have you ever seen restaurant owner feel disappointed as there are haters intentionally make the restaurants rating lower, but their food and services is actually good.

##### Note: Due to time limit, we are focusing on the first two problem statements.

## Solution:

#### 1) Using Selenium and Beautiful Soup to extract the food & beverage list, their reviews and also find out which restaurants has halal certification by JAKIM or other halal certification body. We are not using google apis here as the free tier limit is 500 at maximum.

#### 2) The f&b and reviews data will be scrape from Google Maps directly. On the other hand, halal certification status will be scrape from www.halal.gov.my or www.verifyhalal.com.

#### 3) Build Django dashboard with the wordcloud feature to summarise the dishes or topics which people thought about the restaurant.

## Scope of Location:

### Should I focus on areas which have:

#### 1) less malay populations and less obvious malay shops? 5 votes
##### or 
#### 2) more malay populations and more malay shops? 1 vote

### Based on research, I have selected top 5 locations: Subang Jaya, Puchong, Seri Kembangan, Petaling Jaya, Cheras

## Scope of F&B Category:

#### Halal Food, Western Food, Fast Food, Vegetarian Food, Chinese Food, Indian Food, Malay Food, Middle Eastern Food, Japanese Food, Korean Food, Cafe, Dessert

## Git Basic Commands

#### 1) ```git checkout -b your-branch-name```
#### 2) ```git add .``` or the specific file you want to add e.g. tests.py
#### 3) ```git commit -m "add your specific commit message here"```
#### 4) ```git push --set-upstream origin your-branch-name```

## Semantic Commit Messages

#### 1) ```feat```: (new feature for the user, not a new feature for build script)
#### 2) ```fix```: (bug fix for the user, not a fix to a build script)
#### 3) ```docs```: (changes to the documentation)
#### 4) ```style```: (formatting, missing semi colons, etc; no production code change)
#### 5) ```refactor```: (refactoring production code, eg. renaming a variable)
#### 6) ```test```: (adding missing tests, refactoring tests; no production code change)
#### 7) ```chore```: (updating grunt tasks etc; no production code change)

## Git Other Commands
#### 1) ```git rm --cached your-folder-or-file-name``` if you have issues of tracking your files

## Command to import data from CSV
#### ```python manage.py import_fnb_data```