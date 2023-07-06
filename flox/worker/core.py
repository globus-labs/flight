import lightning as L

from flox.worker.base import AbstractWorkerLogic


def work(worker_id, logic: AbstractWorkerLogic, module: L.LightningModule, **kwargs):
    trainer = L.Trainer(
        accelerator=kwargs.get("accelerator", "auto"),
        devices=kwargs.get("devices", 1),
        max_epochs=kwargs.get("max_epochs", 3)
    )
    data_loader = kwargs["data_loader"]  # logic.on_data_retrieve()
    trainer.fit(module, data_loader)
    return {
        "worker_id": worker_id,
        "global_module": module
    }
