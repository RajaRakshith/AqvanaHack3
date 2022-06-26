# Aqvana
This is Aqvana, a portmanteau of Aqua and Nirvana, symbolizing our hope that this app will provide a insight into the background of our drinking water.

# Usage
Our product is an SMS alert system using Twilio. Using publicly available databases, we evaluate the water quality using the nine parameters of the 
water quality index. Through the application, users are able to input their zip code and get alerts on the water quality in their area.

# Description
We used a variety of different techniques to build our project. We first started by coding it in python and using different libraries such as Pandas, 
in order to read and modify the excel files as DataFrames, and we used NumPy to calculate the linear regression for the value of our variables, such 
as nitrite nitrogen content, turbidity, and more, and the WQI. In addition, we used Twilio in order to send a text message alert with the WQI for a 
particular date. We pulled the data from GemStat, the UN water quality database which gave us data to explore the parameters.

# Installation
Download the repository and insert the API Keys for Twilio. Then, you can run this program in python.

# Further Information

Check out our devpost: https://devpost.com/software/aqvana
