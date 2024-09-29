import argparse

from arpeggio.interpreter import interpret
from arpeggio.parser import Parser


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="arpeggio", description="Interpret Arpeggio source code into audio."
    )

    subparsers = parser.add_subparsers(title="commands", required=True, dest="command")

    play_parser = subparsers.add_parser("play", help="Play an Arpeggio file")
    play_parser.add_argument("source", help="Arpeggio file to interpret")

    compile_parser = subparsers.add_parser(
        "compile", help="Compile an Arpeggio file to WAV"
    )
    compile_parser.add_argument("source", help="Arpeggio file to interpret")
    compile_parser.add_argument("output", help="Output file to write")

    args = parser.parse_args()

    with open(args.source) as f:
        source = f.read()
    ast = Parser().parse(source, wrap_errors=False)
    song = interpret(ast)

    if args.command == "compile":
        song.render().export(args.output, format="wav")
        print(f"Exported to {args.output}")
        return

    song.play()


if __name__ == "__main__":
    main()
