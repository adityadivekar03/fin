from iexfinance.iexdata import get_tops
import json


tops = get_tops(["AAPL"])
print(tops)

print('jsonifying...')

print(json.loads(tops[0]))