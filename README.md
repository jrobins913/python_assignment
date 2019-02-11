# README #

Python Big10 web site stats scraping assignment

The project includes 3 files:
crawl.py
calc.py
db.py

The crawl.py file is the first script to run and will scrape the stats from the big10 site for each team and load 2 tables with batting stats and pitching stats.
The script is setup to run against sqllite or postgresql defaulted to sqllite so you can run the code completely standalone.  You can change the database
uncommenting the appropriate line at the top of crawl.py and calc.py

The calc.py file runs queries against the tables loaded from crawl and displays the results on the console.  I filtered the results somewhat as data outliers
were skewing results and he standard deviation.  Basically, made sure batters had at least 10 plate appearances and pitchers threw at least 10 innings.

The db.py file has convenience functions for the ORM that I used called peewee.  The ORM handles the table creation and provides a fast way to interact
with the database.  This makes it easy to change database backends and eliminates having to deal with ddl directly. (postgresql password needs to be set in here if running with postgresql).

To Run (libraries are checked into repo so you may not need to run the pip commands!)
pip install beautifulsoup4
pip install requests
pip install peewee
pip install html5lib
pip install lxml

If running against postgresql, make sure you have the python driver loaded and set the username and password in the db.py file
pip install psycopg2-binary

Then run crawl.py to scrape and load tables
Then run calc.py to view results