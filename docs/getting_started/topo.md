## What is a Topology?
Federated Learning is done over a scattered collection of devices that collectively 
train a machine learning model. In Flight, we refer to the topology that defines these 
devices and their connectivity as a ***Topology***.

## Creating Topologies
The ``flight.topo`` module contains the code needed to define your own ``Topology`` 
networks. They are built on top of the ``NetworkX``  library. Generally speaking, to 
create ``Topology`` instances in FLoX, we provide two interfaces:
  1. interactive mode
  2. file mode

Interactive mode involves creating a ``NetworkX.DiGraph()`` object directly and then 
passing that into the ``Topology`` constructor. This is **not** recommended.

The recommended approach is ***file mode***. In this mode, you define the Topology 
instance using a supported file type (e.g., `*.yaml`) and simply use it to create 
the Topology instance.

```python
from flight.topo import Topology

topo = Topology.from_yaml("my_topo.yaml")
```

***

# Endpoint YAML Configuration

```yaml
rpi-0:
  globus-compute-endpoint: ... # required
  proxystore-endpoint: ...     # required
  children: [rpi-1]            # required
  resources:
    num_cpus: 2
    num_gpus: 0.5

rpi-1:
  ...

...
```