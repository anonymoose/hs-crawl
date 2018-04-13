
# "Write a multi-threaded web crawler in python in 30 minutes."

Uses Requests library to get a webpage and BeautifulSoup to pull out the links.  Multiple threads to run in parallel.  True parallelism would use Multiprocessing library.

## Run it

```
./run --seed https://somesite.com/ --workers 2

```

