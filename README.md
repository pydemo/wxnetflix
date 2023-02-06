# wxnetflix
wxpython netflix demo

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