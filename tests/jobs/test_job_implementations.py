from flight.jobs.aggregation import AggregateJob, DebugAggregateJob
from flight.jobs.local_training import DebugLocalTrainJob, LocalTrainJob
from flight.jobs.protocols import AggregableJob, TrainableJob


def test_protocol_implementations():
    assert isinstance(AggregateJob(), AggregableJob)
    assert isinstance(DebugAggregateJob(), AggregableJob)
    assert isinstance(LocalTrainJob(), TrainableJob)
    assert isinstance(DebugLocalTrainJob(), TrainableJob)
