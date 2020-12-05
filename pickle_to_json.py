import pickle
import json

with open("bachelor_data_pickle_updated", "rb") as f:
    data = pickle.load(f)

with open("bachelor_data.json", "w+", encoding="utf8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open("assoc_data_pickle_updated", "rb") as f:
    data = pickle.load(f)

with open("assoc_data.json", "w+", encoding="utf8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

