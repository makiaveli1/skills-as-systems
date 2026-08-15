import argparse
import json
from pathlib import Path


def _load_routes():
    repository_root = Path(__file__).resolve().parents[2]
    with (repository_root / "config" / "routes.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def render_route(name):
    routes = _load_routes()
    return f"route {name} -> {routes[name]}"


def main():
    parser = argparse.ArgumentParser(prog="relaypack")
    parser.add_argument("name")
    args = parser.parse_args()
    try:
        print(render_route(args.name))
    except KeyError:
        parser.error(f"unknown route: {args.name}")


if __name__ == "__main__":
    main()
