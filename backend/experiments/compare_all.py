import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from backend.experiments.common import execute, parser

def main():
    args = parser("Compare paired VRP algorithms under static and dynamic traffic").parse_args()
    execute(args)

if __name__ == "__main__": main()
