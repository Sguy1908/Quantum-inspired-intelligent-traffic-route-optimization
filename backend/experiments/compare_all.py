if __package__ in {None, ""}:
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.experiments.common import execute, parser

def main():
    args = parser("Compare paired VRP algorithms under static and dynamic traffic").parse_args()
    execute(args)

if __name__ == "__main__": main()
