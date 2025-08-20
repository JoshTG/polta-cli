"""
A screen for the metastore app that displays available tables.
"""
from deltalake import DeltaTable
from polars import DataFrame, read_delta
from os import path
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import DataTable, DirectoryTree, Footer, Header, Input, Label

from polta_cli.widgets.delta_table_tree import DeltaTableTree


class TablesScreen(Screen):
  """The screen to view metastore tables"""
  BINDINGS = [
    ('escape', 'clear_filters', 'Clear table filters'),
    ('m', 'toggle_metadata_columns', 'Toggle metadata columns')
  ]
  include_metadata_columns: reactive = reactive(True)
  table_path: reactive[str] = reactive('')
  filters: reactive[str] = reactive('')

  def on_mount(self) -> None:
    """Execute on screen mount"""
    self.query_exactly_one('#tree-table').focus()
    self.query_exactly_one('#tree-table', DeltaTableTree).root.expand_all()

  def compose(self) -> ComposeResult:
    """Compose main UI
    
    Returns:
      compose_result (ComposeResult): the resulting UI
    """
    yield Header()
    yield Footer()
    with Vertical():
      with Horizontal():
        yield DeltaTableTree(
          path=path.join(self.app.main_path, 'tables'),
          id='tree-table',
          name='Table'
        )
        with VerticalScroll(can_focus=False, can_focus_children=False):
          yield Label('Number of rows: N/A', id='lbl-rowcount')
          yield Label('Version: N/A', id='lbl-version')
          yield Label('Partitions: N/A', id='lbl-partitions')
          yield Label('\nSchema: N/A', id='txt-schema')
      with Horizontal():
        with VerticalScroll(can_focus=False):
          yield Input(
            placeholder='id = "abc" AND active_ind = false',
            id='input-table-filter'
          )
          yield DataTable(
            zebra_stripes=True,
            id='dt-table'
          )

  @on(Input.Submitted)
  def update_table(self, value: Input.Submitted) -> None:
    """Updates table when the filter is updated
    
    Args:
      value (Input.Submitted): the new filter conditions
    """
    self.filters: reactive[str] = value.value
    self.update_table_view()

  @on(DirectoryTree.DirectorySelected)
  def new_directory(self, selected: DirectoryTree.DirectorySelected) -> None:
    """Runs when a directory tree selects a new table
    
    Args:
      selected (DirectoryTree.DirectorySubmitted): the selected directory
    """
    self.table_path: reactive[str] = str(selected.path)
    self.action_clear_filters()

  def action_clear_filters(self) -> None:
    """Clears the table filters and updates the table"""
    self.filters: reactive[str] = ''
    self.query_exactly_one('#input-table-filter', Input).clear()
    self.update_table_view()

  def update_table_view(self) -> None:
    """Updates the table view"""
    if not self.table_path:
      return
    if not DeltaTable.is_deltatable(self.table_path):
      return
        
    dt: DeltaTable = DeltaTable(self.table_path)
    df: DataFrame = read_delta(self.table_path)

    if self.filters:
      try:
        df: DataFrame = df.sql(f'SELECT * FROM self WHERE {self.filters}')
      except Exception as e:
        self.notify(
          message=str(e),
          title='Table Filter Error',
          severity='error',
          timeout=10
        )

    table: DataTable = self.query_exactly_one(DataTable)
    table.clear(columns=True)

    if not self.include_metadata_columns:
      df: DataFrame = df.drop([c for c in df.columns if c.startswith('_')])

    for column in df.columns:
      table.add_column(column)

    for row in df.rows():
      table.add_row(*row)
    
    self.query_exactly_one('#lbl-version', Label).update(f'Version: {dt.version()}')
    self.query_exactly_one('#lbl-partitions', Label).update(f'Partitions: {", ".join(dt.metadata().partition_columns)}')
    self.query_exactly_one('#lbl-rowcount', Label).update(f'Number of rows: {df.shape[0]}')
    fields: list[str] = [f'{name} ({dtype})' for name, dtype in df.schema.items()]
    self.query_exactly_one('#txt-schema', Label).update('\nSchema:\n  ' + '\n  '.join(fields))

  def action_toggle_metadata_columns(self) -> None:
    """Toggles the metadata columns value"""
    self.include_metadata_columns: bool = not self.include_metadata_columns
    self.update_table_view()
