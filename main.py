import sys
import os
if __name__ == "__main__":
    location=sys.argv[1]
    if os.path.exists(location):
        print(location)
    else:
        print("location not found")    
