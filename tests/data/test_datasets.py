from pathlib import Path

import pandas as pd
import torch
from sklearn.datasets import make_classification

# TODO: Get rid of `sklearn` as a dependency.
from torch.utils.data import Dataset

from flight.data import FederatedSubsets, LocalDataset, federated_split
from flight.topo import Topology
from flight.topo.states import NodeState

##################################################################################################################


class MyDataDir(LocalDataset):
    def __init__(self, state: NodeState, csv_dir: Path):
        super().__init__(state)
        csv_path = csv_dir / f"{state.idx}" / "data.csv"
        self.data = pd.read_csv(csv_path)
        self.csv_path = csv_path

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        x = torch.tensor([[row.x1], [row.x2]])
        y = torch.tensor([row.y])
        return x, y

    def __len__(self):
        return len(self.data)


########################################################################################


class MyRandomDataset(Dataset):
    def __init__(self, n_classes: int):
        super().__init__()
        data_sk = make_classification(
            n_samples=100, n_features=20, n_classes=n_classes, random_state=1
        )
        x_sk, y_sk = data_sk
        x_torch = torch.from_numpy(x_sk)
        y_torch = torch.from_numpy(y_sk)
        y_torch = y_torch.unsqueeze(dim=-1)
        self.data_torch = torch.hstack((x_torch, y_torch))

    def __getitem__(self, idx: int):
        datum = self.data_torch[idx]
        x, y = datum[:-1], datum[-1]
        y = y.to(torch.int)
        return x, y

    def __len__(self):
        return len(self.data_torch)


def test_fed_subsets():
    topo = Topology.from_yaml("examples/topos/2-tier.yaml")
    data = MyRandomDataset(n_classes=2)
    fed_data = federated_split(
        data, topo, num_classes=2, samples_alpha=1.0, labels_alpha=1.0
    )
    assert isinstance(fed_data, (dict, FederatedSubsets))
