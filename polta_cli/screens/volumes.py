"""
A screen for the metastore app that displays available volumes.
"""
from os import path, startfile
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import DirectoryTree, Footer, Header

from polta_cli.widgets.delta_table_tree import DeltaTableTree


class VolumesScreen(Screen):
  """The screen to view metastore volumes"""

  def on_mount(self) -> None:
    """Execute on screen mount"""
    self.query_exactly_one('#tree-ingestion').focus()
    self.query_exactly_one('#tree-ingestion', DirectoryTree).root.expand_all()
    self.query_exactly_one('#tree-quarantine', DeltaTableTree).root.expand_all()
    self.query_exactly_one('#tree-export', DirectoryTree).root.expand_all()

  def compose(self) -> ComposeResult:
    """Compose main UI
    
    Returns:
      compose_result (ComposeResult): the resulting UI
    """
    volume_path: str = path.join(self.app.main_path, 'volumes')

    yield Header()
    yield Footer()
    with Horizontal():
      with VerticalScroll(can_focus=False):
        yield DirectoryTree(
          path=path.join(volume_path, 'ingestion'),
          id='tree-ingestion',
          name='Ingestion'
        )
      with VerticalScroll(can_focus=False):
        yield DeltaTableTree(
          path=path.join(volume_path, 'quarantine'),
          id='tree-quarantine',
          name='Quarantine'
        )
    with Horizontal():
      with VerticalScroll(can_focus=False):
        yield DirectoryTree(
          path=path.join(volume_path, 'exports'),
          id='tree-export',
          name='Export'
        )

  @on(DirectoryTree.FileSelected)
  def open_file(self, selected: DirectoryTree.FileSelected) -> None:
    """Opens a selected file with the default system program for that file type
    
    Args:
      selected (DirectoryTree.FileSelected): the selected file
    """
    file_path: str = str(selected.path)
    startfile(file_path)
