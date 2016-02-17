##Sanisbury Test
=====================


Prepare Local Enviornment
--------------------------

Requires Python 2.7 or higher
Install dependencies: `sudo pip install -r requirements.txt`

if pip does not work try following commands on linux:
`apt-get remove python-pip`
`easy_install pip`

Install python 2.7.x or higher version from https://www.python.org/downloads/
or use following commands
 - wget https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz 
 - tar xzvf Python-2.7.6.tgz 
 - cd Python-2.7.6.tgz
 - ./configure
 - sudo make
 - sudo make install

Its very simple script and can be run using simple python console.
 - Go to <python location> (e.g. /usr/bin/python)
 -  run script using command as: 
	python web_crawler.py 

- Outputs a JSON string as below:

Sample output:
```
Scrapping starts here.............
{
    "result": [
        {
            "description": "Apricots", 
            "size": "38.27kb", 
            "title": "Sainsbury's Apricot Ripe & Ready x5", 
            "unit_price": 3.5
        }, 
        {
            "description": "Avocados", 
            "size": "38.67kb", 
            "title": "Sainsbury's Avocado Ripe & Ready XL Loose 300g", 
            "unit_price": 1.5
        }, 
        {
            "description": "Avocados", 
            "size": "43.44kb", 
            "title": "Sainsbury's Avocado, Ripe & Ready x2", 
            "unit_price": 1.8
        }, 
        {
            "description": "Avocados", 
            "size": "38.68kb", 
            "title": "Sainsbury's Avocados, Ripe & Ready x4", 
            "unit_price": 3.2
        }, 
        {
            "description": "Conference", 
            "size": "38.54kb", 
            "title": "Sainsbury's Conference Pears, Ripe & Ready x4 (minimum)", 
            "unit_price": 1.5
        }, 
        {
            "description": "Gold Kiwi", 
            "size": "38.56kb", 
            "title": "Sainsbury's Golden Kiwi x4", 
            "unit_price": 1.8
        }, 
        {
            "description": "Kiwi", 
            "size": "38.98kb", 
            "title": "Sainsbury's Kiwi Fruit, Ripe & Ready x4", 
            "unit_price": 1.8
        }
    ], 
    "total": 15.1
}
Scrapping ends here.............
```

##Tests
Run tests with
from location as sainsbury_crawler/tests$ python -m unittest test_web_crawler
or
`python -m unittest test.test_web_crawler -v`
for tests with verbose output

