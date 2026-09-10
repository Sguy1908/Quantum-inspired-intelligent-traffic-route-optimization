from backend.experiments.common import execute, parser
def main(): execute(parser("Run PSO on paired VRP instances").parse_args(), "pso")
if __name__ == "__main__": main()
