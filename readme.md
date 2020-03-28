This tool main contribution is to tie together the Covid-19 data from *Johns Hopkins CSSE* to actual country facts from https://restcountries.eu. That means, for any given country, one can retreive both the COVID-19 time series and the trivia of that country (population, area, world coordinates, etc.) This is done through a lookup table that links the *Johns Hopkins CSSE* country names to country data via their [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code.

The tool fetches both country facts and Covid-19 online data and build an easy to access database linking both together, allowing for example to plot the number of declared cases *per million inhabitants*.

Usage: *covid.py* [-huo FOLDER] [-n <count>]  
       *covid.py* [-huo FOLDER] [-c "countrylist"]  

Options.  
-h --help    show this  
-u --update  update database from online source  
-o --output FOLDER    specify output folder instead of opening web browser  
-n count --number count number of countries to display [default: 10]  
-c "list" --countries "list" space separared list of ISO 3166-1 alpha-2 country code  
  
This depends 2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE available at https://github.com/CSSEGISandData/COVID-19.git

The data is automatically fetched if necessary
