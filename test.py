from clients.sqlite import SqliteClient
from providers.dummy import DummyProvider

prov = DummyProvider()
prov.poll_rate = 5
prov.track_rate = 40
client = SqliteClient(prov, "test.sqlite")
client.run()
