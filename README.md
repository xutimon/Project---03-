# Project 03
This is the [link](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03) to the project instructions. 

The `ebay-dl.py` file in this repositiory is a web scraper that scrapes ebay based on a given specific search term. Specifically, it scrapes the first 10 pages of the results of a search term looking for item names, the items' price, what the items' status is, shipping costs (if any), whether the items have free returns, and how many of the items has been sold (if the information is availible). Note that for me personally, it seems that ebay's anti-bot detector begins to kick in at page 5 of any given search term. 

To run this scrapper in the command line, you simply have to type in the following. This will return the results in a json file. 

```
$python3 ebay-dl.py 'search term' 

```

If you prefer the results to be a csv file, use the following. 

```
$python3 ebay-dl.py 'search term' --csv

```


