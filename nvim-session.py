#!/usr/bin/env python3

import argparse
from functools import wraps
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
from typing import List, Tuple
import sys


SESSIONS_DIR = Path(tempfile.gettempdir()) / 'nvim-sessions'


def ensure_sessions_dir(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        return f(*args, **kwargs)
    return wrapper


class Session:
    def __init__(self) -> None:
        pass

    @staticmethod
    @ensure_sessions_dir
    def attach(path: Path, args: List[str]) -> None:
        sys.stdout.flush()
        os.execlp('dtach', 'dtach', '-A', str(path), '-z', '-e', '^q', '-r', 'ctrl_l', 'nvim', *args)

    @staticmethod
    def exists(name: str) -> bool:
        return (SESSIONS_DIR / name).is_socket()

    @staticmethod
    @ensure_sessions_dir
    def list() -> List[Path]:
        return [x for x in SESSIONS_DIR.iterdir() if x.is_socket()]

    @staticmethod
    def format_list(sess_list: List[Path]) -> str:
        if not sess_list:
            return 'No available sessions! You can make one with -a.'
        sess_fmt = ' * {}'
        fmt = textwrap.dedent("""
            Available Sessions:
            {}
        """)
        return fmt.format('\n'.join([sess_fmt.format(sess.name) for sess in sess_list]))


KnownArgTuple = Tuple[argparse.Namespace, List[str]]


def parse_args(argv: List[str]) -> KnownArgTuple:
    examples = textwrap.dedent("""
        Manage dtach instances of neovim processes.

        Attach to or create the session 'ctf':
        {name} -a ctf

        List sessions:
        {name} -l

        Any leftover arguments will be passsed directly to neovim.
    """.format(name=argv[0]))
    ap = argparse.ArgumentParser(prog=argv[0], description=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--attach', '-a',
        help='Attach to or create a session'
    )
    ap.add_argument('--list', '-l',
        help='List existing sessions',
        action='store_true'
    )
    return ap.parse_known_args(args=argv[1:])


def main(argv: List[str]) -> None:
    args, rest = parse_args(argv)
    if args.list:
        print(Session.format_list(Session.list()))

    if args.attach:
        Session.attach(SESSIONS_DIR / args.attach, rest)


if __name__ == '__main__':
    main(sys.argv)
