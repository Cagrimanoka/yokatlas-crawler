import pickle

with open("assoc_data_pickle", "rb") as f:
    data = pickle.load(f)

with open("assoc_data_pickle_new", "rb") as f:
    new_data = pickle.load(f)

data.update(new_data)

with open("assoc_data_pickle_updated", "wb") as f:
    pickle.dump(data, f, protocol=4)

with open("bachelor_data_pickle", "rb") as f:
    data = pickle.load(f)

with open("bachelor_data_pickle_new", "rb") as f:
    new_data = pickle.load(f)

data.update(new_data)

with open("bachelor_data_pickle_updated", "wb") as f:
    pickle.dump(data, f, protocol=4)