import os
from sqlalchemy import create_engine
from six.moves.configparser import ConfigParser
import subprocess
import argparse
import uuid

parser = argparse.ArgumentParser()
parser.add_argument(
    "--config", required=True,
    help="Please provide configuration ini file as: python add_zip_views.py --config=<config_file.ini>")
args = parser.parse_args()
config = args.config

parser = ConfigParser()
parser.read(config)

db_string = parser.get('app:main', 'sqlalchemy.url')
db = create_engine(db_string)

query = "insert into resource_view (id, resource_id, title, description, view_type, \"order\") \
         select '{}', id, name, description, coalesce('zip_view'), coalesce(0) from resource where format='ZIP' \
         and id not in (select resource_id from resource_view where view_type like 'zip_view');".format(uuid.uuid4())

db.execute(query)

subprocess.call(["ckan", "-c", "{}".format(config), "search-index", "rebuild", "-e", "-i"],
                  cwd="/usr/lib/ckan/py3/src/ckan")

