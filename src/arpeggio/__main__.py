import argparse

from .interpreter import interpret
from .parser import Parser


def main():
    parser = argparse.ArgumentParser(
        prog="arp", description="Interpret Arpeggio source code into audio."
    )

    subparsers = parser.add_subparsers(title="commands")

    play_parser = subparsers.add_parser("play", help="Play an Arpeggio file")
    play_parser.add_argument("source", help="Arpeggio file to interpret")

    compile_parser = subparsers.add_parser(
        "compile", help="Compile an Arpeggio file to WAV"
    )
    compile_parser.add_argument("source", help="Arpeggio file to interpret")
    compile_parser.add_argument("--output", help="Optional output file to write")

    args = parser.parse_args()
    with open(args.source) as f:
        source = f.read()

    ast = Parser().parse(source, wrap_errors=False)
    song = interpret(ast)

    if getattr(args, "output", None):
        raise NotImplementedError("Output to file not yet implemented")

    song.play()


if __name__ == "__main__":
    main()
