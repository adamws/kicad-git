import os
from pathlib import Path

import pcbnew


def test_if_plugin_loads() -> None:
    dirname = Path(os.path.realpath(__file__)).parents[1]
    pcbnew.LoadPluginModule(dirname, "source", "")
    not_loaded = pcbnew.GetUnLoadableWizards()
    assert not_loaded == "", pcbnew.GetWizardsBackTrace()
