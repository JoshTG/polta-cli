"""
A CLI application to manage a polta metastore.
"""
from os import path
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from polta_cli.screens.tables import TablesScreen


class MetastoreApp(App):
  """CLI app for managing a metastore"""
  CSS_PATH = 'metastore.tcss'
  SCREENS = {
    'tables': TablesScreen
  }
  BINDINGS = [
    ('d', 'toggle_dark', 'Toggle dark mode'),
    ('t', 'push_screen("tables")', "Tables"),
    ('e', 'quit', 'Exit')
  ]

  def __init__(self, main_path: str) -> None:
    self.main_path: str = main_path
    super().__init__()

  def compose(self) -> ComposeResult:
    """Compose main UI
    
    Returns:
      compose_result (ComposeResult): the resulting UI
    """
    yield Header()
    yield Footer()

  def on_mount(self) -> None:
    """Execute on screen mount"""
    self.push_screen('tables')
    self.title: str = path.basename(self.main_path)

  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode"""
    self.theme = (
      'textual-dark' if self.theme == 'textual-light' else 'textual-light'
    )

def main() -> None:
  from sys import argv
  app: App = MetastoreApp(main_path=argv[1])
  app.run()



if __name__ == '__main__':
  main()
