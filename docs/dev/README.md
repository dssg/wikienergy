Developer Guide
===============

This guide outlines best practices for developers

Style Conventions
-----------

Please follow standard style described in
(PEP-8)[http://legacy.python.org/dev/peps/pep-0008/]

Testing
-------

Tests can be run from the test directory by following the instructions in the
README there.

Autogenerating Documentiation
-----------------------------

Documentation is generated using the sphinx tool. Documentation can be
cleaned and regenerated using the following commands:

    make clean
    make html

Here is an example of a good docstring for a method:

    def concatenate_traces(traces[,how="strict"]):
        '''Concatenates the list of traces.

        :param traces: The ApplianceTraces you wish to concatenate.
        :type traces: list of ApplianceTrace objects.
        :param how: method for concatenation.
        :type how: "strict".
        :rtype: ApplianceTrace.

        '''
        # code goes here

Classes, modules and packages should also have docstrings, which come on the
first line of their declarations (or the `__init__.py` file for packages).

A class docstring:

    class MyPublicClass(object):
        """We use this as a public class example class.

        You never call this class before calling :func:`public_fn_with_sphinxy_docstring`.

        .. note::

           An example of intersphinx is this: you **cannot** use :mod:`pickle` on this class.

        """

A module docstring (on the first line of the file):

    """
    .. module:: useful_1
       :platform: Unix, Windows
       :synopsis: A useful module indeed.

    .. moduleauthor:: Phil Ngo <phil@invalid.com>


    """

Additional examples may be found
(here)[https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example].
