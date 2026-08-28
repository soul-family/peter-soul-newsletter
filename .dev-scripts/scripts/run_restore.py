import sys
from pathlib import Path

sys.path.insert(0, str(Path('.').resolve() / '.dev-scripts'))

from shared.encoding_utils import restore_windows1252

fixed, errors = restore_windows1252(Path('src-preps'))
print(f'Fixed: {fixed}, Errors: {errors}')
