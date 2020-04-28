#覚書
#!/bin/sh
screengit push origin master

python3 bitcoingen.py
echo ^Ad

split -l 500000 -d -a 3 richlist.csv ./list/list_ --additional-suffix=.csv

cat *.csv > ../richlist.csv