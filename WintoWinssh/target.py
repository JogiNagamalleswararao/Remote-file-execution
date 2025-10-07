import sys
import platform
import socket
import datetime

def main():
    # Arguments passed from controller
    args = sys.argv[1:]
    
    print("=== Target Script Execution ===")
    print(f"Time: {datetime.datetime.now()}")
    print(f"Host: {socket.gethostname()} ({socket.gethostbyname(socket.gethostname())})")
    print(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Python: {platform.python_version()}")
    
    if args:
        print(f"Arguments: {args}")
    else:
        print("No arguments provided.")

    # Example: simple operation
    print("Performing calculation: sum of [1..10]")
    print("Result =", sum(range(1, 11)))

if __name__ == "__main__":
    main()
