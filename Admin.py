# from InvoiceXML import Files
from pymongo import MongoClient


# A = Files()


client = MongoClient()
db = client.primer
coll = db.dataset

# cursor = db.primer.find()
# for document in cursor:
#     print(document)

print(db.primer.count())
