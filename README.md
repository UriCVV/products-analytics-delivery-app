## INTRODUCTION & QUESTIONS 

You’ve been given a data set about orders coming from Fake partners in the app. Fake 
partners are the stores that are not integrated with our Delivery app directly so our 
content team manages their product catalog and prices for them. Fake partner orders are 
charged to the customer upon delivery and in many cases there is a mismatch between 
the total amount at checkout in the app (products_total) and what the courier pays at the 
store (p urchase_total_price) causing many problems. When the products_total is lower 
than purchase_total_price we call them under-authorized orders, otherwise is a 
correctly authorized order. We want to move away from charge-on-delivery to an 
authorize-and-capture model but we first need to understand the price fluctuation of 
past orders to know the risk of doing so.  
Dataset description:  
• -  order_id  
• -  activation_time_local: local time when the order was activated  
• -  country_code  
• -  store_address  
• -  final_status  
• -  payment_status  
• -  products: number of products in the order  
• -  products_total: total amount at checkout (€)  
• -  purchase_total_price: amount the courier paid at the store (€)  


#### <u>questions:</u>
1. What percent of orders are under-authorized?  
2. What percent of orders would be correctly authorized w/ incremental 
authorisation  
(+20%) on the amount at checkout?  
3. Are there differences when split by country?  
4. For the remainder of orders that would be outside of incremental auth what 
values would be necessary to capture the remaining amount?  
5. Which stores are the most problematic in terms of orders and monetary value?  
6. For under-auth orders is there a correlation between the difference in the prices 
and  
the cancellation of the order? In other words: Is an order more likely to be 
cancelled as the price difference increases?  
 
## PROCESS

#### STEP 1 : CLEANING

1- NAMING COLUMNS as the csv files has no haders 
2- NaN VALUES : not exist, not need to drop them
3- 

#### QUESTION 1. What percent of orders are under-authorized?

1- new column "money_difference_percentaje" which gives us the precentaje difference between 'purchase_total_price' and 'products_total'
2- FUNCTION: "check_orders" :a simple mathematical equation will answer this question comparing the leght of the  total df and the subset lenght when applied the
    condition "money money_difference" < 0. 

#### QUESTION 2. What percent of orders would be correctly authorized w/ incremental authorisation  (+20%) on the amount at checkout? 
 Just running again the function "check_orders" function again changing the condition to "money money_difference" > 20 gives us the answer. 



#### QUESTION 3. Are there differences when split by country?

  Function "check_by_group" has been defined. It takes three parameters:
      -dataframe
      -operator (greater, lower, equal...)
      -value (the value we want to get as a reference and which, together with the operator, will set the filtering criteria)
      - p_typte : it can be shop or country 
    This function will return us a df with the top 10 countries or stores after filtering. 
  Tn answer this question it is just needed to run funciont "check_by_group" using "country" as the p_type. 
  Two filtering conditions are used:
      1- money_difference_percentaje < 0
      2- money_difference_percentaje > 20
      
   as both criteria reflect bad performance. A merge of both dataframes returns the most problematic countries /stores.
   
   Visualization function "count_plot" let us visualize the above reults.
   Function "scatter_plot" also reveals valuable information regarding global dataframe information indicating that some countries
   may not have the highest number of "problematic" orders.

#### QUESTION 4. For the remainder of orders that would be outside of incremental auth what values would be necessary to capture the remaining amount?
 
 A new column ('capture_amount') is created in order to answer this questions.
 capture_amount = (products_total *1.2)-purchase_total_price
 
#### QUESTION 5. Which stores are the most problematic in terms of orders and monetary value? 

The process to answer this question has been the same as for question 3 but using 'store_address' as a parameter instead of 'country_code' int hte check_by_group function

#### QUESTION 5.For under-auth orders is there a correlation between the difference in the prices and  the cancellation of the order? In other words: Is an order more likely to be cancelled as the price difference increases? 

In order to answer this question we have made the average of purchase_total_price and results do not show correlation
between the amount of the order and its status
 
 
 ## CONCLUSIONS
 
 1-more than 50% of orders are out of the "desirable" margin
 2-Spain and Argentina should be the countries to focus on as they are the ones with highest values of problematic ordersf
 3-Chile,though not being in the "top" countries regaring problematic orders, is the country with highest percentaje difference orders so, would also be interesting to make a dipper look on it
 4- the capture amount so all ordes are above 20% is, in average, 1.35
 5-It does not seem to be correlation between the price of the order and its cancellation.