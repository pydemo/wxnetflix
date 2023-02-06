# wxnetflix
wxpython netflix demo

## ushow.bat
Shows filterable list of netflis items from in/netflix_titles_2021.csv


```
C:\Users\alex_\myg\wxnetflix>cat ushow.bat
python ui.py  -nop 2 -r DEV -p csv/show/data -pa config.yml netflix_titles_2021.csv  %*
```
Opens to:
![List of all items](docs/screenshots/ushow.jpg)
