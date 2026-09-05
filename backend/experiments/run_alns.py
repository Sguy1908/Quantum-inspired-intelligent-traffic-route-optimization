from backend.experiments.common import execute, parser
def main(): execute(parser("Run ALNS on paired VRP instances").parse_args(), "alns")
if __name__ == "__main__": main()
