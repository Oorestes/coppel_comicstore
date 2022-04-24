import hashlib
from datetime import datetime

from comicstore.settings import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY

def get_marvel_hash():
    ts = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
    params = {
        'ts': ts,
        'apikey': MARVEL_PUBLIC_KEY,
        'hash': hashlib.md5(f'{ts}{MARVEL_PRIVATE_KEY}{MARVEL_PUBLIC_KEY}'.encode('utf-8')).hexdigest()
    }
    return params
    