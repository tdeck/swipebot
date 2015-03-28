from providers.reddit import RedditProvider
from clients.sqlite import SqliteClient
from pprint import pprint

prov = RedditProvider('worldnews')
client = SqliteClient(prov, "reddit.sqlite")
print "Starting client..."
client.run()
