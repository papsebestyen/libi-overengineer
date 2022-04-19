from invoke import task
from src.forecast import train_forecaster, get_prediction
import pickle
from pathlib import Path
from src.get_data import get_data
from tempfile import TemporaryDirectory
from datetime import datetime
from src.s3 import FileStorage
from pathlib import Path


@task
def lint(ctx):
    ctx.run(f"black src")
    ctx.run(f"isort src --profile black")
    ctx.run(f"flake8 src")


@task
def upload_data(cli):
    tmp_dir = TemporaryDirectory()
    get_data(datetime.now(), Path(tmp_dir.name))
    storage = FileStorage()
    for file in Path(tmp_dir.name).iterdir():
        storage.upload_bytes(file.read_bytes(), file.name)
    tmp_dir.cleanup()


@task
def retrain_forecaster(cli):
    forecaster = train_forecaster()
    Path("src/models/forecaster.pickle").write_bytes(pickle.dumps(forecaster))

@task
def upload_prediction(cli):
    storage = FileStorage()
    prediction = get_prediction()
    storage.upload_bytes(prediction.to_frame().to_parquet(), 'prediction.parquet')
