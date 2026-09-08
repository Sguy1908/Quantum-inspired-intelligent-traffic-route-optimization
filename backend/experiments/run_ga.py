if __package__ in {None, ""}:
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.experiments.common import execute, parser
def main(): execute(parser("Run GA on paired VRP instances").parse_args(), "ga")
if __name__ == "__main__": main()
