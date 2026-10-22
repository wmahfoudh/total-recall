# Backups

The archives of this folder, one per backup, the whole folder apart
from `backup/`. `/total-recall backup` writes an archive ending in
`-manual`, and `/total-recall update` writes one ending in `-auto`
before it changes a file. Old archives are deleted by hand.

To restore an archive, extract it at the root of the project:
`tar -xzf "<internal folder>/backup/<archive>"`.
