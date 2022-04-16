from invoke import task

@task
def download_data(cli):
    from src.download.get_data import get_data
    from pathlib import Path
    from datetime import datetime

    data_path = Path('data')
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