import pickle
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from invoke import task

from src.forecast import get_prediction, train_forecaster
from src.get_data import get_data
from src.s3 import FileStorage


@task
def lint(ctx):
    ctx.run("black . -l 79")
    ctx.run("isort . --profile black")
    ctx.run("flake8 . --max-line-length=79")


@task
def upload_data(cli):
    tmp_dir = TemporaryDirectory()
    get_data(datetime.now(), Path(tmp_dir.name))
    storage = FileStorage()
    for file in Path(tmp_dir.name).iterdir():
        storage.upload_bytes(file.read_bytes(), file.name)
    tmp_dir.cleanup()


@task
def retrain_model(cli):
    forecaster = train_forecaster()
    Path("src/models/forecaster.pickle").write_bytes(pickle.dumps(forecaster))


@task
def upload_prediction(cli):
    storage = FileStorage()
    prediction = get_prediction()
    storage.upload_bytes(
        prediction.to_frame().to_parquet(), "prediction.parquet"
    )


@task
def deploy_api(cli):
    cli.run("sudo systemctl start libi")
    cli.run("sudo systemctl enable libi")
    cli.run("sudo systemctl start nginx")
    cli.run("sudo systemctl enable nginx")
