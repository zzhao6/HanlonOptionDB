from timeout import *
from time import *

if __name__ == "__main__":
    with timeout(seconds=1):
        try:
            sleep(2)
        except TimeoutError as err:
            print("handelled")
            print(err)
