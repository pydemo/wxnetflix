# wxnetflix
wxpython netflix demo


## Data source
https://www.kaggle.com/datasets/swatikhedekar/exploratory-data-analysis-on-netflix-data/code?resource=download


# Installation
```
virtualenv --python=/usr/bin/python3.6 <path/to/new/virtualenv/>
source <path/to/new/virtualenv>/bin/activate
pip install -r requirements.txt
```


## ufinal.bat/Data search
Shows data and and lets you filter items for in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ufinal.bat
python ui.py  -nop 2 -r DEV -p csv/show/data_plot -pa config.yml netflix_titles_2021.csv  %*
```


### All data
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ushow.JPG)

Then navigate to "Filter" text input control in upper panel and start typing.

### Filtered data
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ushow_ukraine.JPG)

## ${\color{red}Note: \space Plotting \space is \space always \space done \space over \space full \space data \space set.}$
__`Filtering will not affect plotting!`__


## ufinal.bat/Plot 1
Shows data and first plot "Release by type"  for in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ufinal.bat
python ui.py  -nop 2 -r DEV -p csv/show/data_plot -pa config.yml netflix_titles_2021.csv  %*
```
Then navigate to first tab ("Release by type") in lower panel and click "Plot" Button

### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ufinal.JPG)


## ufinal.bat/Plot 2
Shows data and second plot "Count by ratings" for in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ufinal.bat
python ui.py  -nop 2 -r DEV -p csv/show/data_plot -pa config.yml netflix_titles_2021.csv  %*
```
Then navigate to second tab ("Count by ratings") in lower panel and click "Plot" Button

### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ufinal_2.JPG)


## ufinal.bat/Plot 3
Shows data and third plot "Count by type" for in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ufinal.bat
python ui.py  -nop 2 -r DEV -p csv/show/data_plot -pa config.yml netflix_titles_2021.csv  %*
```
Then navigate to third tab ("Count by type") in lower panel and click "Plot" Button

### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ufinal_3.JPG)


## ufinal.bat/Plot 4
Shows data and forth plot "Count by year" for in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ufinal.bat
python ui.py  -nop 2 -r DEV -p csv/show/data_plot -pa config.yml netflix_titles_2021.csv  %*
```
Then navigate to forth tab ("Count by year") in lower panel and click "Plot" Button

### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ufinal_4.JPG)


## ufinal.bat/Plot 5
Shows data and fifth plot "Count by year" for in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ufinal.bat
python ui.py  -nop 2 -r DEV -p csv/show/data_plot -pa config.yml netflix_titles_2021.csv  %*
```
Then navigate to fifth tab ("Count by year") in lower panel and click "Plot" Button

### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ufinal_5.JPG)





