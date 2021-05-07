
import sys
# https://gist.github.com/eriky/daec8b4a4e4082103e6c0d736ea0d5ff#file-check_python_version-py

if not sys.version_info > (2, 7):
   # berate your user for running a 10 year
   # python version
    print ("bad")
elif not sys.version_info >= (3, 5):
   # Kindly tell your user (s)he needs to upgrade
   # because you're using 3.5 features
   print("worse")
elif not sys.version_info >= (7, 8):
   # Kindly tell your user (s)he needs to upgrade
   # because you're using 3.5 features
   print("you are dreaming")
