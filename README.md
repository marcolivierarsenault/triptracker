# Trip Tracker

Building a small website to track my trip to mexico price. If ever it goes bellow 4k, I can go ahead and ask for a price match.

## Goal

The lambda function run 4 times a day and fetch the price of the trip from <https://voyagesarabais.com/> website. The I use Dash to display a very simple view of the price history.

## Run

Simply launch the container:

```bash
docker run -p 8050:8050 --env aws_access_id=XXXXX --env aws_access_secret=XXXXX marcolivierarsenault/triptracker
```

## Build

basic docker style:

```bash
docker build -t triptracker .
```

## Now track my trip

Unless you bought it at the same place that might be highly un-usefull for you.
