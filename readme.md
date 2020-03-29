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

## Usage
Usage: **covid.py** [-hpu] [-d | -r] [-s | -a] [-o *FILE*] [-n *count*] [-i "*includelist*"] [-b *start*] [-x "excludelist"] [-w *smoothing_window_size*] [-c *cipping_days*]

| Options                      | Explanations                                                                                                                                                           |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -h --help                    | Show help                                                                                                                                                              |
| -u --update                  | Update database from online [default: False]source                                                                                                                                     |
| -o --output FILE             | Specify output file name instead of opening web browser                                                                                                                |
| -n count --number count      | Number of top countries to display. Set to 0 for displaying only a custom list (along with the -c option). Set to -1 to display all countries. [default: 10]           |
| -b start --begin start       | Starting point (first day the number of case/death reach that level) [default: 100]                                                                                    |
| -c days --clip days          | Clip the plot to this number of days. Zero (0) means an unbounded graph.  [default: 0]                                                                                      |
| -s --speed                   | Plot the progression rate (speed) instead of the cummulative case [default: False]                                                                                     |
| -a --acceleration            | Plot the variation of the progression rate (acceleration) instead of the cummulative case [default: False]                                                             |
| -i "list" --include "list" | Space separared list of [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)                                                                         |
| -x "list" --exclude "list"   | Space separared list of [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)                                                                         |
| -w size --window size        | Smooting window size. Curves are soothed using an order 3 polynomial fit on a moving window of size 2n+1 the given number. Set to 0 to prevent smoothing and display raw data. [Default: 3] |
| -p --population              | Plot the numbers as a ratio of the country population (by million inhabitants) [default: False]                                                                        |
| -d --deaths                  | Use data from the deaths reports instead of the declared cases [default: False]                                                                        |
| -r --recovered               | Use data from the recovered reports instead of the declared cases [default: False]                                                                        |

This depends 2019 Novel Coronavirus COVID-19 (2019-nCoV) [Data Repository by Johns Hopkins CSSE available](https://github.com/CSSEGISandData/COVID-19.git) and the country facts from [REST COUNTRIES](https://restcountries.eu).

## Examples
`# Display in a web browser the top 10 countries in term of cummulated number of declared cases`  
`>python covid.py`  

`# Display in a web browser the top 5 countries in term of cummulated number of declared cases`  
`>python covid.py -n 5`  

`# Save in a file speed of declared cases for Spain, France and Italy`  
`>python covid.py -o c:\temp\plot.html -sc "ES FR IT"`  

`# Display in a web browser the number of cases by million inhabitants for the top 10 countries in term of cummulated declared cases. Start the curves when the number of cases gets bigger than 500.`  
`>python covid.py -pb 500`  

`# Fetch latest data and display in a web browser the top 10 countries in term of cummulated number of declared cases.`  
`>python covid.py -u`  

`# Compare only Canada and U.S.A. in term of declared cases relative to their respective population (per 1M inhabitants)`  
`>python covid.py -c "CA US" -pn0`  

`# Compare Iceland plus the top 5 countries excluding China and U.S.A. Display the new cases per day relative to country population (per 1M inhabitants)`  
`>python covid.py -c "IS" -spn5 -x "CN US"`  

`# Compare top 3 countries raw cummulative data without any curve smoothing`  
`>python covid.py -w 0 -n3`  

`# Compare the death rate raw data from top ten countries`  
`>python covid.py -sdw0`  

`# Display in a web browser the number of cases for the top 10 countries, starting when the cases reach 1000 and stoping after 30 days.`  
`>python covid.py -b 1000 -c30`  


## Example of what is easily available inside the code
`canada = database['CA']`  
`numpy_array = canada['timeseries']`  
`population = canada['info']['population']`  
`death_by_million = numpy_array[-1] / population * 1e6`  

### References
This depends 2019 Novel Coronavirus COVID-19 (2019-nCoV) [Data Repository by Johns Hopkins CSSE available](https://github.com/CSSEGISandData/COVID-19.git) and the country facts from [REST COUNTRIES](https://restcountries.eu).
