from os import getcwd, path
from polta.metastore import Metastore


# The sample metastore for testing / instructional purposes
metastore: Metastore = Metastore(
  main_path=path.join(getcwd(), 'sample', 'sample_metastore')
)
