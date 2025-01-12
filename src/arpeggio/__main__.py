import argparse
import os
from collections.abc import Callable

from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from arpeggio.interpreter import InterpreterError, interpret
from arpeggio.parser import Parser, ParsingError


def _parse_play(command_parser) -> argparse.ArgumentParser:
    parser = command_parser.add_parser("play", help="Play an Arpeggio file")
    parser.add_argument("source", help="Arpeggio file to interpret")
    parser.add_argument(
        "-w", "--watch", action="store_true", help="Re-play on file change."
    )
    return parser


def _parse_compile(command_parser) -> argparse.ArgumentParser:
    parser = command_parser.add_parser(
        "compile", help="Compile an Arpeggio file to WAV"
    )
    parser.add_argument("source", help="Arpeggio file to interpret")
    parser.add_argument("output", help="Output file to write")
    parser.add_argument(
        "-w", "--watch", action="store_true", help="Re-compile on file change."
    )
    return parser


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="arpeggio",
        description="Interpret Arpeggio source code into audio.",
    )

    command_parser = parser.add_subparsers(
        title="commands", required=True, dest="command"
    )
    _parse_play(command_parser)
    _parse_compile(command_parser)

    return parser.parse_args()


class WatchedFileHandler(FileSystemEventHandler):
    def __init__(self, modified_callback):
        self.modified_callback = modified_callback
        self.last_modified = 0.0

    def on_modified(self, event: FileModifiedEvent) -> None:
        # File changes trigger two events. Use mtime to dedupe
        modified = os.stat(event.src_path).st_mtime
        if modified == self.last_modified:
            return

        self.last_modified = modified
        self.modified_callback()


def _watch_file(path: str, *, callback: Callable[[], None]):
    event_handler = WatchedFileHandler(modified_callback=callback)
    observer = Observer()
    observer.schedule(event_handler, path=path, event_filter=[FileModifiedEvent])
    observer.start()

    print(f"Watching {path} for changes (CTRL + C to exit)...")
    try:
        while observer.is_alive():
            observer.join(1.0)
    except KeyboardInterrupt:
        # TODO: If the thread is playing, just interrupt it instead of exiting.
        observer.stop()
        print("Exiting...")
    finally:
        observer.stop()
        observer.join()


def _render_file(path: str, output: str | None = None):
    with open(path) as f:
        source = f.read()

    try:
        ast = Parser().parse(source, wrap_errors=True)
        song = interpret(ast)
    except (ParsingError, InterpreterError) as e:
        print(e)
        return

    if output:
        song.render().export(output, format="wav")
        return

    song.play()


def main() -> None:
    args = _parse_args()
    output = args.output if args.command == "compile" else None

    def render():
        _render_file(path=args.source, output=output)

    # Run once, then start watching
    render()
    if args.watch:
        _watch_file(path=args.source, callback=render)


if __name__ == "__main__":
    main()
