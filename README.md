### *python* web-server based on *coroutines*

####Docker:

```
docker build -t tp-highload-hw1 .
docker run -p 80:80 -v httpd.conf:/etc/httpd.conf:ro -v /Users/nadezda/Desktop/tp-highload-hw1/http-test-suite:/var/www/html:ro tp-highload-hw1:latest
```

#### Tests:
```
cd http-test-suite
python2 httptest.py
```
 