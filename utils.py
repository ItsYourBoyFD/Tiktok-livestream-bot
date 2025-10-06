import os, sys

def clearConsole():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')
    else:
        pass

def setConsoleTitle(Content):
    global DebugMode
    if os.name == 'posix':
        sys.stdout.write(f"\33]0;{Content}\a")
        sys.stdout.flush()
        return False
    elif os.name == 'nt':
        os.system(f"title {Content}")
        return False
    else:
        pass

def readFile(filename,method):
    with open(filename,method,encoding='utf8') as f:
        content = [line.strip('\n') for line in f]
        return content

def readProxiesFile():
    path = os.path.join("Data", "Proxies.txt")
    try:
        return readFile(path, 'r')
    except Exception:
        print("Warning: Proxies.txt not found. Continuing without proxies.")
        return []