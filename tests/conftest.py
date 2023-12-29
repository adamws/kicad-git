from pathlib import Path

import pytest
from dulwich.repo import Repo


@pytest.fixture()
def repo(tmpdir: Path) -> Repo:
    repo = Repo.init(tmpdir)
    config = repo.get_config()
    config.set("user", "email", "test@pytest")
    config.set("user", "name", "pytest")
    config.write_to_path()
    return repo
