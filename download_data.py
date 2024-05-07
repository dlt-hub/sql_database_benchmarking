from nids_datasets import Dataset, DatasetInfo
from time import time

df = DatasetInfo(dataset='UNSW-NB15')

t1 = time()
print(f"Dataset info: {df}")

dataset = 'UNSW-NB15'
subset = [
    'Network-Flows',
    # 'Packet-Fields',
    # 'Payload-Bytes',
] # or 'all' for all subsets
files = [1,2,3,4,5,6,7] # or 'all' for all files

data = Dataset(dataset=dataset, subset=subset, files=files)
data.download()

print(f"Time: {time() - t1:.2f} seconds")