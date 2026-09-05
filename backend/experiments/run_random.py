from backend.experiments.common import execute, parser
def main(): execute(parser("Run random search on paired VRP instances").parse_args(), "random")
if __name__ == "__main__": main()
