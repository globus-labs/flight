import os
import sys
from pathlib import Path
import multiprocessing
import time

import pandas as pd
import torch
from torch import nn
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor

try:
    sys.path.append("..")
    from flight.data.utils import federated_split
    from flight.topo import Topology
    from flight.nn import FloxModule
    from flight.runtime.fit import federated_fit
    from flight.strategies.impl.fedavg import FedAvg
except Exception as e:
    raise ImportError("unable to import FloX libraries") from e


# Default safe path for datasets
if "TORCH_DATASETS" not in os.environ:
    os.environ["TORCH_DATASETS"] = "./data"  # set fallback default


class MyModule(FloxModule):
    def __init__(self, lr: float = 0.01):
        super().__init__()
        self.lr = lr
        self.last_accuracy = torch.tensor(0.0)  # required by federated_fit

        self.flatten = torch.nn.Flatten()
        self.linear_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.linear_stack(x)

    def training_step(self, batch, batch_idx):
        inputs, targets = batch
        preds = self(inputs)
        loss = torch.nn.functional.cross_entropy(preds, targets)

        # Track accuracy
        correct = (preds.argmax(dim=1) == targets).sum().item()
        total = targets.size(0)
        acc = correct / total
        self.last_accuracy = torch.tensor(acc)

        return loss

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=self.lr)


def main():
    multiprocessing.set_start_method("spawn", force=True)
    print("Multiprocessing start method:", multiprocessing.get_start_method())

    # Build topology
    topo = Topology()
    leader = topo.add_node(kind="leader")
    topo.leader = leader

    for i in range(3):
        worker = topo.add_node(kind="worker")
        topo.add_edge(leader.idx, worker.idx)
        print(f"Worker {i} added: idx={worker.idx}, kind={worker.kind}")

    # Load dataset
    mnist = FashionMNIST(
        root=os.environ.get("TORCH_DATASETS", "./data"),  # fallback path
        download=True,
        train=True,
        transform=ToTensor(),
    )

    # Federated split
    fed_data = federated_split(mnist, topo, 10, 1.0, 1.0)
    print(f"Type of fed_data: {type(fed_data)}, len: {len(fed_data)}")

    for i, shard in enumerate(fed_data):
        print(f"  Shard {i}: type={type(shard)}")
        try:
            node_id, dataset = shard
            print(f"    NodeID: {node_id}, dataset size: {len(dataset)}")
        except Exception as e:
            print(f"    Failed to unpack or access dataset: {e}")

    # Run federated_fit
    print("\n>>> Starting federated_fit with multiprocessing...")
    start_time = time.time()

    try:
        _, df = federated_fit(
            topo,
            MyModule(),
            fed_data,
            5,
            strategy=FedAvg()
        )
        df["strategy"] = "fed-avg"
        print(">>> federated_fit completed successfully.")

    except Exception as e:
        print(">>> ERROR during federated_fit():", e)
        raise

    duration = time.time() - start_time
    print(f">>> federated_fit took {duration:.2f} seconds")

    # Save results
    train_history = df.reset_index(drop=True)
    Path("out").mkdir(exist_ok=True)
    train_history.to_feather(Path("out/federated_history.feather"))
    print(">>> Finished and saved training log to out/federated_history.feather")


if __name__ == "__main__":
    main()

