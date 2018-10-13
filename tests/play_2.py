s = "/Users/fanjialiang2401/Desktop/flask/hello_flask/logs/acesslog.log"

import os

if not os.path.exists(s):
    with open(s, "w"):
        pass

else:
    print("sd")
