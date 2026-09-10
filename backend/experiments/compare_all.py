from backend.experiments.common import execute, parser

def main():
    args = parser("Compare paired VRP algorithms under static and dynamic traffic").parse_args()
    execute(args)

if __name__ == "__main__": main()
