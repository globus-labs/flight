"""
This module defines _Federated Learning **Processes**_. FL Processes come in two flavors:

+ Synchronous
+ Asynchronous

The former breed of FL Process (namely, synchronous) is the most widely-studied in the literature and is the only
one of the two that (currently) supports hierarchical execution.
"""

from flight.runtime.process.process_async import AsyncProcess
from flight.runtime.process.process_sync import SyncProcess

__all__ = ["AsyncProcess", "SyncProcess"]
