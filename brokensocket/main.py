def run_server():
    from brokensocket.Server import start_server
    start_server()
def run_client():
    from brokensocket.Client import start_client
    start_client()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BrokenSocket CLI")
    parser.add_argument("mode", choices=["server", "client"], help="Run as server or client")
    args = parser.parse_args()
    if args.mode == "server":
        run_server()
    elif args.mode == "client":
        run_client()

if __name__ == "__main__":
    main()
