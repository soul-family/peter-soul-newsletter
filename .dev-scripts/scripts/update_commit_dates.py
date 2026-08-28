#!/usr/bin/env python3
"""
update_commit_dates.py — set file meta dates in each src-preps/commit folder
to the corresponding blog post creation date from date_map.csv.

Sets all three timestamps:
- Date created (creation time)
- Date modified (modification time)
- Date accessed (access time)

- commit1..commitN: date = blog post contained in that commit
- commit0-familytree: date = first column post date (july_2002)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.paths import PREPS, DATE_MAP
from shared.csv_utils import load_date_map

if sys.platform == 'win32':
    import ctypes
    from ctypes import wintypes

    HANDLE = wintypes.HANDLE
    LPFILETIME = ctypes.POINTER(wintypes.FILETIME)

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    CreateFileW = kernel32.CreateFileW
    CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                            wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, HANDLE]
    CreateFileW.restype = HANDLE

    SetFileTime = kernel32.SetFileTime
    SetFileTime.argtypes = [HANDLE, LPFILETIME, LPFILETIME, LPFILETIME]
    SetFileTime.restype = wintypes.BOOL

    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = [HANDLE]
    CloseHandle.restype = wintypes.BOOL

    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    OPEN_EXISTING = 3
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

    def dt_to_filetime(dt):
        ft = wintypes.FILETIME()
        unix_ts = dt.timestamp()
        filetime_ts = int((unix_ts + 11644473600) * 10_000_000)
        ft.dwLowDateTime = filetime_ts & 0xFFFFFFFF
        ft.dwHighDateTime = (filetime_ts >> 32) & 0xFFFFFFFF
        return ft

    def set_windows_times(path, target_dt):
        handle = CreateFileW(
            str(path),
            GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        if handle == wintypes.HANDLE(-1).value:
            return False
        try:
            ft = dt_to_filetime(target_dt)
            if not SetFileTime(handle, ctypes.byref(ft), ctypes.byref(ft), ctypes.byref(ft)):
                return False
            return True
        finally:
            CloseHandle(handle)
else:
    def set_windows_times(path, target_dt):
        return False

def set_dates(dir_path, target_dt):
    ts = target_dt.timestamp()
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            p = Path(root) / name
            try:
                os.utime(p, (ts, ts))
            except OSError:
                pass
            if sys.platform == 'win32':
                try:
                    set_windows_times(p, target_dt)
                except OSError:
                    pass
        for d in dirs:
            dp = Path(root) / d
            try:
                os.utime(dp, (ts, ts))
            except OSError:
                pass
            if sys.platform == 'win32':
                try:
                    set_windows_times(dp, target_dt)
                except OSError:
                    pass

def set_dates_from_map(cdir, dm):
    for root, dirs, files in os.walk(cdir):
        for name in files:
            p = Path(root) / name
            rel = str(p.relative_to(PREPS)).replace('\\', '/')
            if rel in dm and dm[rel] is not None:
                target_dt = dm[rel]
                ts = target_dt.timestamp()
                try:
                    os.utime(p, (ts, ts))
                except OSError:
                    pass
                if sys.platform == 'win32':
                    try:
                        set_windows_times(p, target_dt)
                    except OSError:
                        pass
        for d in dirs:
            dp = Path(root) / d
            rel = str(dp.relative_to(PREPS)).replace('\\', '/')
            if rel in dm and dm[rel] is not None:
                target_dt = dm[rel]
                ts = target_dt.timestamp()
                try:
                    os.utime(dp, (ts, ts))
                except OSError:
                    pass
                if sys.platform == 'win32':
                    try:
                        set_windows_times(dp, target_dt)
                    except OSError:
                        pass

def main():
    dm = load_date_map(DATE_MAP)
    first_blog_date = None
    commit_blog = {}

    for rel, dt in dm.items():
        if '/content/columns/' in rel:
            if first_blog_date is None or dt < first_blog_date:
                first_blog_date = dt
            fname = rel.split('/')[-1]
            commit_blog[fname] = dt

    commits = sorted([d for d in PREPS.iterdir() if d.is_dir() and d.name.startswith('commit')])

    for cdir in commits:
        name = cdir.name
        if name == 'commit0-familytree':
            if first_blog_date:
                set_dates(cdir, first_blog_date)
                print(f'{name}: set to first blog date {first_blog_date.date()}')
            continue

        if name == 'commit0':
            set_dates_from_map(cdir, dm)
            print(f'{name}: set dates from date map')
            continue

        blog_files = list(cdir.rglob('*.html'))
        blog_dates = []
        for bf in blog_files:
            fname = bf.name
            if fname in commit_blog:
                blog_dates.append(commit_blog[fname])

        if not blog_dates:
            print(f'{name}: no blog post found, skipping')
            continue

        target = min(blog_dates)
        set_dates(cdir, target)
        print(f'{name}: set to {target.date()} ({len(blog_dates)} blog post(s))')

if __name__ == '__main__':
    main()
