# wxnetflix
wxpython netflix demo


## ufinal.bat
Shows data and 5 plots  for in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ufinal.bat
python ui.py  -nop 2 -r DEV -p csv/show/data_plot -pa config.yml netflix_titles_2021.csv  %*
```
### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ufinal.JPG)


## uplot.bat
Shows rating/count scatterplot for  in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat uplot.bat
python ui.py  -nop 2 -r DEV -p csv/plot/data -pa config.yml netflix_titles_2021.csv  %*
```
### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/uplot_ratings_count.JPG)


## ushow.bat
Shows filterable list of in/netflix_titles_2021.csv items.

```
C:\Users\alex_\myg\wxnetflix>cat ushow.bat
python ui.py  -nop 2 -r DEV -p csv/show/data -pa config.yml netflix_titles_2021.csv  %*
```
### Opens to
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ushow.JPG)

### Filtering
![List of all items](https://github.com/pydemo/wxnetflix/blob/main/docs/screenshots/ushow_ukraine.JPG)






