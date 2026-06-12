Application to capture and display Analysts Ratings for stocks of interest 

Admin accounts created: admin / test123
User account created: user1 / test123

List of changes after 03/03:
Created Models for Portfolio and Holdings. Add to Admin site
Create ModelForm to create new Portfolio records
Add menu entry to access Portfolio form
Create PortfolioForm.html to display form
In Project urls.py change default path from '/stocks' to ''
In stocks/urls.py add PortfolioCreate and PortfolioUpdate
In stocks/views.py add views for PortfolioCreate and PortfolioUpdate
In stocks/urls.py add holdingcreate and holdinglist
in stocks/views.py add views for HoldingCreate and HoldingList

