# Welcome to Flight

### Getting Started
Flight is a simple, highly customizable, and easy-to-deploy framework for launching Federated Learning processes across a
decentralized network. It is designed to simulate FL workflows while also making it trivially easy to deploy them on
real-world devices (e.g., Internet-of-Things and edge devices). Built on top of _Globus Compute_ (formerly known as
_funcX_), Flight is designed to run on anything that can be started as a Globus Compute Endpoint.


### What can Flight do?

Flight supports several state-of-the-art approaches for FL processes, including hierarchical and asynchronous FL.

|     |      2-tier      |   Hierarhchical   |
| --: |:----------------:|:-----------------:|
| **Synchronous**| :material-check: | :material-check:  |
| **Asynchronous** | :material-check: | :material-close:  |


#### Installation

The package can be found on, and installed from, GitHub. Installation is done with the
following CLI call:

```bash
pip install git+https://github.com/globus-labs/flight
```

#### Usage

Flight is a simple, highly-customizable, and easy-to-deploy framework for hierarchical, multi-tier federated learning
systems built on top of the Globus Compute platform.

```python title="Basic Flight Example" linenums="1"
from flight import Topology, federated_fit
from torch import nn


class MyModule(nn.Module):
    ...


topo = Topology.from_yaml("my_topo.yaml")
federated_fit(
    module=MyModule(),
    topo=topo,
    strategy="fedavg",
    strategy_params={"participation_frac": 0.5},
    where="local",
    logger="csv",
    log_out="my_results.csv"
)
```


