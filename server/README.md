## Server
======


### Install
-------

Install Server::

    $ pip install -e .

Run
---

::

    $ export FLASK_APP=manage:app
    $ export FLASK_ENV=development
    $ flask run

Open http://127.0.0.1:5000/metrics in a browser.


### Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

```sh
sudo pip3 install -r requirements/dev.txt
pytest --cov-report term --cov=project tests/
=========================================================================================== test session starts ====================================================================================
platform linux -- Python 3.6.8, pytest-3.7.4, py-1.8.0, pluggy-0.12.0
rootdir: /home/user/git/revolut/server, inifile: setup.cfg
plugins: testinfra-1.19.0, pylint-0.14.0, cov-2.7.1
collected 12 items                                                                                                                                                                                         

tests/test_app.py ..........                                                                                                                                                                         [ 83%]
tests/test_models.py ..                                                                                                                                                                              [100%]

----------- coverage: platform linux, python 3.6.8-final-0 -----------
Name                  Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------
project/__init__.py      24      1      0      0    96%
project/app.py           79     14     18      4    81%
project/config.py        19      1      2      1    90%
project/models.py        20      1      2      1    91%
-------------------------------------------------------
TOTAL                   142     17     22      6    86%


======================================================================================== 12 passed in 0.48 seconds =================================================================================
```
