Tests
=====

How to run the tests
--------------------

The entire test suit can be run using the following command:

    python -m unittest discover

If you wish to run only the fast tests, use the following:

    python fast_test_suite.py

If you wish to execute or write tests with greater specificity, see the full
documentation (linked below).

Settings in `tests/settings.py` should be updated to include the proper
credentials.

Information
-----------

We use python's builtin `unittest` module, documentation for which can be found
[here](https://docs.python.org/2/library/unittest.html).
