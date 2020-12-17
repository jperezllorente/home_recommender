# YOUR RIGHT PLACE ON EARTH 

## Overview
As a final project for the Ironhack bootcamp on Data Analytics I decided to create a home recommender that would tak into account, 
not only the characteristics of the house, but also the characteristics of the area in which it is located. This means that 
the user can decide what kind of establishments he wants to have near the place he is going to live in, like sport facilities, 
restaurants and nightclubs, or pharmacies. 

I decided to make this project because I've always wondered what it would be to choose where I would like to live by something
more than the price or the number of rooms of a house. Of course, I can check this information using other means, but I wanted
to be able to check all this variables at the asme time. 

## Resources and Libraries

## Process

### 1. Data Extraction and preparation

For this project I used two APIs: Idealista and Foursquare. From the former I extracted all the information related to homes that were being rented;
and from Foursquare I obtained the location (latitude, longitude) and name of different establishments like restaurants, hospitals and gyms. 

The data from Idealista needed a bit of work before I stored it in my database, so I used regex, duplicates(), isnull() and other functions from Pandas to clean and prepare it. 
Once this was done, I inserted both dataframes in two different MongoDb collections: **homes** and **places**


## 2. Geo queries and home selection

To create de home selector I had to divide the process in three steps. First, I created a function from which I obtained the objects from the **places** collection that belonged to
a certain category and were located near the houses from the homes collection. To do this I used the $near function from Mongo, which returns a list of dictionaries with all the 
objects that are located inside a specified radio that has each of the homes as its radio. 

The categories currently available are:
- Restaurants and Nightlife
- Hospitals
- Pharmacy
- Gyms
- Parks
- Supermarkets
- School
- Transport
- Entertainment

Once I got a list with aa lsita of the objects near each of the houses, I counted the number of objects in each list and if the total was greater than a certain limit, that home was selected. Each
category has its own limit (gym has a limit of 700 metres, hospitals has a limit of 3000 metres and entertainment a limit of 1500 metres), so I had to create a function for each of the existing
categories, which is note very efficient (this would be a future improvement). 

Finally, I created a function that returned a dataframe with the homes that fulfilled all the criteria chosen by the user. Here is important ot point out that as I have one function for each 
of the categories, the initial result would be three dataframes, one for each category. So, in order to get just one dataframe and delete all duplicates, I concatenated all three dataframes and 
added a code line that selected only those rows that appeared more than once and then deleted all duplicates. This way, I make sure that the elements from the final selection belong to 
at least two of the three categories. At the beggining I wanted to select only those homes that belonged to all three categories, but as I don't have enough data the results were scarce, and I 
decided to change the limit. Also, with the objective of creating a better recommender, I added three more variables related to the characteristics of the selected houses. 

The criteria a user can choose from are:
- Category_1, Categroy_2 and Category_3: each of this have their own scrolling menu and created their own dataframe to be concatenated later
- District: in which district oyu want te he house to be located
- Price: the range of prices between which you are interested in
- Property Type: flat, duplex or penthouse

## 3. API creation 

The final product is an API that has three endpoints.

The first one, and base for the other two, is a form in which the user selects the criteria he is interested in. There are 6 dropdown menus, one for each criteria, and two submit buttons that 
are connected to the other endpoints: Map and Table. If the user clicks on the Map button, he will be taken to another page with a map (created using folium) of madrid and the markers for all 
the selected homes; and if he clicks on the Table button he will see a dataframe with all the home's information. 

## 4. Future improvements

The first would be to improve the efficiency of the code so that the execution time is reduced. This can be probably be done by modifying the functions used so that I don't have to use of for each
the categories, but rather have only one that can change depending on the argument given. 

In order to have a proper product, I have to add a lot more data to the database, not only in terms of quantity, but also in terms of quality, specially in what refers to geographical 
distribution. Here, it would be great to have a function that could extract all the information from Foursquare without having to choose a different location each time. 

To improve the search scope, I can add more criteria like rooms or floor. Also, it would be a good idea to have submenus for each of the places' categories, like types of food in restaurants, 
or education style in a school. However, to achieve this I need to complete first the second point about data collection.  

Finally, if I was to scale this to include other regions or countries, I believe it could be a really interesting business idea to develop. 