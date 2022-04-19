import imp
from fastapi import File
from invoke import task


@task
def lint(ctx):
    ctx.run(f"black src")
    ctx.run(f"isort src --profile black")
    ctx.run(f"flake8 src")


@task
def download_data(cli):
    from src.get_data import get_data
    from pathlib import Path
    from datetime import datetime

    data_path = Path("data")
    data_path.mkdir(exist_ok=True)

    get_data(datetime.now(), data_path)


@task
def upload_new_data(cli):
    from src.get_data import get_data
    from tempfile import TemporaryDirectory
    from datetime import datetime
    from src.s3 import FileStorage
    from pathlib import Path

    tmp_dir = TemporaryDirectory()
    get_data(datetime.now(), Path(tmp_dir.name))

    storage = FileStorage()
    for file in Path(tmp_dir.name).iterdir():
        storage.upload_bytes(file.read_bytes(), file.name)

    tmp_dir.cleanup()

@task
def retrain_forecaster(cli):
    from src.forecast import train_forecaster
    import pickle
    from pathlib import Path
    forecaster = train_forecaster()
    Path('src/models/forecaster.pickle').write_bytes(pickle.dumps(forecaster))

