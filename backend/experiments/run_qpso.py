from backend.experiments.common import execute, parser
def main(): execute(parser("Run QPSO on paired VRP instances").parse_args(), "qpso")
if __name__ == "__main__": main()
