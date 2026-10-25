"""Command line: `uv run cheatsheet build` and `uv run cheatsheet serve`."""

import argparse
import logging
import sys
from pathlib import Path

from cheatsheet.build import CONTENT_DATA, CONTENT_DIR, SITE_OUT_DIR, build_content, build_site, write_content_data
from cheatsheet.content import ContentError
from cheatsheet.serve import make_server


def main() -> None:
    parser = argparse.ArgumentParser(prog="cheatsheet", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="run every example, then build the static site")
    build.add_argument("--content", type=Path, default=CONTENT_DIR, help="content folder (default: content/)")
    build.add_argument("--out", type=Path, default=SITE_OUT_DIR, help="site output folder (default: site/dist/)")
    build.add_argument("--base", default="/", help="URL path the site is served under (default: /)")
    serve = commands.add_parser("serve", help="serve the built site locally")
    serve.add_argument("--dir", type=Path, default=SITE_OUT_DIR, help="folder to serve (default: site/dist/)")
    serve.add_argument("--port", type=int, default=4321)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.command == "build":
        try:
            data = build_content(args.content)
        except ContentError as error:
            sys.exit(f"Content error: {error}")
        write_content_data(data, CONTENT_DATA)
        build_site(CONTENT_DATA, args.out, args.base)
        print(f"Built the site in {args.out}")
    else:
        if not (args.dir / "index.html").is_file():
            sys.exit(f"No built site in {args.dir}; run `uv run cheatsheet build` first")
        server = make_server(args.dir, args.port)
        print(f"Serving {args.dir} at http://127.0.0.1:{server.server_port}/ (Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
