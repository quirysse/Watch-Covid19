# Introduction
This tool main contribution is to tie together the Covid-19 data from *Johns Hopkins CSSE* to actual country facts from https://restcountries.eu. That means, for any given country, one can retreive both the COVID-19 time series and the trivia of that country (population, area, world coordinates, etc.) This is done through a lookup table that links the *Johns Hopkins CSSE* country names to country data via their [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code.

The tool fetches both country facts and Covid-19 online data and build an easy to access database linking both together, allowing for example to plot the number of declared cases *per million inhabitants*.

## Main goals of this piece of software:
* Make the link between different country databases: Covid-19 and country facts
* Perform some data analysis on the raw data: curve smoothing, speed and acceleration monitoring, exponential curve fitting, etc.
* Provide graphical summary that is easy to read and easy to share

## Two main sources of data are tied together:
* [REST COUNTRIES](https://restcountries.eu/)
* [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)

## Example of what is possible
`canada = database['CA']`  
`numpy_array = canada['timeseries']`  
`population = canada['info']['population']`  
`death_by_million = numpy_array[-1] / population * 1e6`  

## Usage

Usage: *covid.py* [-hpuo FOLDER] [-s | -a] [-n <count>] [-b <start>]  
       *covid.py* [-hpuo FOLDER] [-s | -a] [-c "countrylist"] [-b <start>]  

Options.  
-h --help    show this  
-u --update  update database from online source  
-o --output FILE    specify output file instead of opening web browser  
-n count --number top number of countries to display [default: 10]  
-b start --begin start starting point (first day the number of case/death reach that level) [default: 100]  
-s --speed   plot the progression rate (speed) instead of the cummulative case [default: False]  
-a --acceleration   plot the variation of the progression rate (acceleration) instead of the cummulative case [default: False]  
-c "list" --countries "list" space separared list of  [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code  
-p --population  plot the numbers as a ratio of the country population (by million inhabitants) [default: False]  

## Examples
`# Display in a web browser the five top countries in term of cummulated number of declared cases`  
`>python covid.py -n 5`  

`# Save in a file speed of declared cases for Spain, France and Italy`  
`>python covid.py -o c:\temp\plot.html -sc "ES FR IT"`  

`# Display in a web browser the number of cases by million inhabitants for the top 10 countries in term of cummulated declared cases. Start the curves when the number of cases gets bigger than 500.`  
`>python covid.py -pb 500`  

`# Fetch latest data and display in a web browser the top 10 countries in term of cummulated number of declared cases.`  
`>python covid.py -u`  

  
### References
This depends 2019 Novel Coronavirus COVID-19 (2019-nCoV) [Data Repository by Johns Hopkins CSSE available](https://github.com/CSSEGISandData/COVID-19.git) and the country facts from [REST COUNTRIES](https://restcountries.eu).
