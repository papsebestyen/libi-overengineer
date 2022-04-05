from invoke import task

@task
def download_data(cli):
    from src.download.get_data import get_data
    from pathlib import Path
    data_path = Path('data')
    data_path.mkdir()
    print(data_path.exists())
    get_data(data_path)