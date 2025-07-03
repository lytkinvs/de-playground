from clickhouse_driver import Client

client = Client(host='localhost', port=9000, user='admin', password='admin')

#
# Select query example
#
table_name = "daily"
query = "select * from {}".format(table_name)
res = client.execute(query)
print(res)

