
This Project is made for only educational perpose

# Zeroda_Scrapping
Scrraping stock and option data from zeroda .This is for educational purpose

Create_WatchList _byClass.py

this script creates watchlist of ce and pe in first and second posiition of your watchlist

ZerodaKiteClass.py :-
this script download data from zeroda

stock_metadata.txt :-
in this file all stocks ,their id is stored 
there is fixed id for stocks 
but options id change from expiry to expiry

so we have to enter updates id the processses will be:
first clear all first 2 watchlist
then run Create_WatchList _byClass.py by using appriopiate input string
then inspect the page 
search for marketwach in network section
the copy the first two pages info fron response of maeketwatch in stock_metadata
make the txt file in same format as i have given

then give input at last of ZerodaKiteClass.py like expirydate and filename in which download reslt to be stored
then run ZerodaKiteClass.py

you will get your downloaded data



