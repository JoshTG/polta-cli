"""
A screen for the metastore app that displays available tables.
"""
from deltalake import DeltaTable
from polars import DataFrame, read_delta
from polars.datatypes import DataType, Datetime
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
  LIMIT_DEFAULT: int = 100

  include_metadata_columns: reactive = reactive(True)
  table_path: reactive[str] = reactive('')
  filters: reactive[str] = reactive('')
  limit: reactive[int] = reactive(LIMIT_DEFAULT)

  def on_mount(self) -> None:
    """Execute on screen mount"""
    self.query_exactly_one('#tree-table').focus()
    self.query_exactly_one('#tree-table', DeltaTableTree).root.expand_all()

    self.query_exactly_one('#col-table-metadata').border_title = 'Table Metadata'
    self.query_exactly_one('#col-table-output').border_title = 'Table Data'
    self.query_exactly_one('#input-table-filter').border_title = 'SQL Filter'
    self.query_exactly_one('#input-table-limit').border_title = 'Result Limit'

  def compose(self) -> ComposeResult:
    """Compose main UI
    
    Returns:
      compose_result (ComposeResult): the resulting UI
    """
    yield Header()
    yield Footer()
    with Vertical():
      with Horizontal():
        with VerticalScroll(
          can_focus=False,
          can_focus_children=False,
          id='col-table-metadata'
        ):
          yield Label('Number of rows: N/A', id='lbl-rowcount')
          yield Label('Version: N/A', id='lbl-version')
          yield Label('Partitions: N/A', id='lbl-partitions')
          yield Label('\nSchema: N/A', id='txt-schema', markup=False)

        yield DeltaTableTree(
          path=path.join(self.app.main_path, 'tables'),
          id='tree-table',
          name='Tables'
        )
      with Horizontal(id='col-table-output'):
        with VerticalScroll(can_focus=False):
          with Horizontal(id='col-table-header'):
            yield Input(
              placeholder='id = "abc" AND active_ind = false',
              id='input-table-filter'
            )
            yield Input(
              value=str(self.LIMIT_DEFAULT),
              type='integer',
              id='input-table-limit'
            )
          yield DataTable(
            zebra_stripes=True,
            id='dt-table'
          )

  @on(Input.Submitted, '#input-table-limit')
  def update_table_limit(self, value: Input.Submitted) -> None:
    self.limit: int = int(value.value or 0)
    self.update_table_view()
    
  @on(Input.Submitted, '#input-table-filter')
  def update_table_filter(self, value: Input.Submitted) -> None:
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
    self.limit: int = 0
    self.query_exactly_one('#input-table-filter', Input).clear()
    self.query_exactly_one('#input-table-limit', Input).value = str(self.LIMIT_DEFAULT)
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

    if self.limit:
      df: DataFrame = df.limit(self.limit)

    for column in df.columns:
      table.add_column(column)
    for row in df.rows():
      table.add_row(*row)

    self.query_exactly_one('#lbl-version', Label).update(f'Version: {dt.version()}')
    partitions_str: str = (f'Partitions: {", ".join(dt.metadata().partition_columns) or "N/A"}')
    self.query_exactly_one('#lbl-partitions', Label).update(partitions_str)
    self.query_exactly_one('#lbl-rowcount', Label).update(f'Number of rows: {df.shape[0]}')
    self.query_exactly_one('#txt-schema', Label).update(self._pretty_print_schema(df.schema))

  def action_toggle_metadata_columns(self) -> None:
    """Toggles the metadata columns value"""
    self.include_metadata_columns: bool = not self.include_metadata_columns
    self.update_table_view()

  def _pretty_print_schema(self, schema: dict[str, DataType]) -> str:
    """Pretty prints schema for the Screen

    Args:
      schema (dict[str, DataType]): the input polars schema
    
    Returns:
      result (str): the pretty schema in string format
    """
    lines: list[str] = ['', 'Schema:']
    for name, dtype in schema.items():
      line: str = f'  {name} {str(dtype).split("(")[0].upper()}'
      if isinstance(dtype, Datetime):
        line += f' {dtype.time_zone}'
      lines.append(line)
    return '\n'.join(lines)