import os
import threading
import time

def run(email, password, n):
    while True:
        try:    os.system(f'python listener.py {email} {password} {n}')
        except: print(f'{WARNING: PROCESS {n} STOPPED: RESTARTING SOON}')
    
def main():
    data = [
            ['lldisposableacc.0@gmail.com', 'lanavedelolvido'],
            ['lldisposableacc.1@gmail.com', 'neoarmstrong'],
            ['lldisposableacc.2@gmail.com', 'lanavedelolvido'],
            ['lldisposableacc.3@gmail.com', 'lanavedelolvido']
        ]

    process = []

    for n, account in enumerate(data):
        process.append(
                threading.Thread(
                    target=run,
                    args=(account[0], account[1], n))
                )
        process[-1].start()
        time.sleep(5)
        try:
            os.remove(".env")
            print(".env removed")
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    main()
