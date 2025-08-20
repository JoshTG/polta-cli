"""
A widget that extends DirectoryTree that only shows directories and delta tables
"""
from deltalake import DeltaTable
from pathlib import Path
from textual.widgets import DirectoryTree
from typing import Iterable


class DeltaTableTree(DirectoryTree):
  """DirectoryTree but only show delta tables and directories"""
  def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
    """Filter paths, including delta tables and directories"""
    return [
      path for path in paths
      if (path.is_dir() and not path.name.startswith('_')) or DeltaTable.is_deltatable(path)
    ]
