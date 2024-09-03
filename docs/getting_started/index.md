Here, we provide a brief high-level overview of how to get started with FLoX.

```python
from flight.run import federated_fit
from flight.topo import Topology

topo = Topology.from_yaml("sample-topo.yml")
results = federated_fit(
    topo, module_cls, datasets, num_global_rounds=10, strategy="fedavg"
)
```