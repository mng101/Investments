Application to capture and display Analysts Ratings for stocks of interest 

Admin accounts created: admin / test123
User account created: user1 / test123

List of changes after 03/03:
Created Models for Portfolio and Holdings. Add to Admin site
Create ModelForm to create new Portfolio records
Add menu enry to access Portfolio form
Create PortfolioForm.html to display form
In Project urls.py change default path from '/stocks' to ''
In stocks/urls.py add PortfolioCreate and PortfolioUpdte
In stocks/views.py add views for PortfolioCreat and PortfolioUpdate

