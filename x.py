import json


docs = open("docs.json", "r")
docs = json.load(docs)

chunks = [docs[i:i + 10] for i in range(0, len(docs), 10)]
for index, chunk in enumerate(chunks):
  json.dump(chunk, open(f"docs{index}.json", "w"), indent=2)
  
pass