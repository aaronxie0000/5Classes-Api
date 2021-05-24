### 5C Classes API
Project Description:
End points to search classes by different attributes. End points to search if a user's watched classes have spots available. Database store what courses each user is watching for.

Scrape the __publicly__ available website: https://portal.claremontmckenna.edu/ics 

Features:
- search by course title or code
  - via Selenium and BS4 scraping and processing for data
- store a user's watched courses 
- given a user, return the details of their watched courses
  - via postgresql, sqlalchemy 
- create, delete and read a user's watched courses
- endpoints for above functionality 
  - via flask, flask-restful, marshmallow

Future project to use this api:
- Send automated email if a watched class has spots that opened (call the endpoint at set interval to determine if send email or not)
