# job_tracking
Tool for tracking target companies, job applications, and application status.

## Initial Requirements ##
- Python 3.9.7
- virtualenv 20.2.2

### Use These Commands to Setup Virtual Environment and Install Additional Requirements ###
- virtualenv -p python3 env
- source env/bin/activate
- python3 -m pip install -U pip
- python3 -m pip install -r requirements.txt

### To-Do ###
- add functionality for sqlite3, may need to create a more generalizable database connection system
- ~~write view to list targets and their most recent activity date~~
- create status to bury a target
- ~~write a view to display the activity log for a particular target/position~~
- create a data model to store database in a hosted environment (GCP, Heroku, etc.)
- create a web interface
- create a Sankey diagram
- verfiy DB table keys and foreign key logic to ensure duplicates are not possible
- refactor psycopg2/SQL to reduce risk of SQL injection

### References ###
- ConfigParser - https://docs.python.org/3/library/configparser.html
- pyscopg / PostgreSQL Quick Reference - https://pynative.com/python-postgresql-tutorial/
- Solution to previously unidentified name shadowing problem - https://stackoverflow.com/a/43768050/8901223
- fancy formatting f-strings - https://www.peterbe.com/plog/how-to-pad-fill-string-by-variable-python