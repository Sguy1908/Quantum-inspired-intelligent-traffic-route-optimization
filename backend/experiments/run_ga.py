from backend.experiments.common import execute, parser
def main(): execute(parser("Run GA on paired VRP instances").parse_args(), "ga")
if __name__ == "__main__": main()
