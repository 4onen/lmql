"""
Utility function to manage cached (serialized)
LMQL runtime components.
"""
import os
import pathlib

CACHE_VERSION = 1
CACHE_DIR = pathlib.Path.home() / ".cache" / "lmql"

def prepare_cache_access():
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        return

    cache_is_valid = False
    cache_version = "<none>"
    try:
        with open(os.path.join(CACHE_DIR, "cache-version"), "r") as f:
            cache_version = f.read()
            cache_is_valid = int(cache_version) == CACHE_VERSION
    except:
        cache_is_valid = False
    if not cache_is_valid:
        print("LMQL cache directory ({}) format is outdated, clearing cache (existing: v{}, runtime: v{})...".format(CACHE_DIR, cache_version, CACHE_VERSION))
        for f in os.listdir(CACHE_DIR):
            os.remove(os.path.join(CACHE_DIR, f))
        with open(os.path.join(CACHE_DIR, "cache-version"), "w") as f:
            f.write(str(CACHE_VERSION))

def cache_file_exists(path):
    prepare_cache_access()
    return os.path.exists(path)

class CacheDirFile:
    def __init__(self, path, mode):
        assert not os.path.isabs(path), "CacheDirFile path must be relative"
        self.path = os.path.join(CACHE_DIR, path)
        self.mode = mode
        self.filehandle = None

    def __enter__(self):
        prepare_cache_access()
        self.filehandle = open(self.path, self.mode)
        return self.filehandle
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.filehandle.close()
        with open(os.path.join(CACHE_DIR, "cache-version"), "w") as f:
            f.write(str(CACHE_VERSION))

def cachefile(path, mode):
    return CacheDirFile(path, mode)