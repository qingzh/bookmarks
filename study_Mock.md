# Unittest in Python
* Mock - Mocking and Testing Library
> mock is now part of the Python standard library, available as *unittest.mock* in Python 3.3 onwards.
> Mock is very easy to use and is designed for use with unittest. Mock is based on the ‘action -> assertion’ pattern instead of ‘record -> replay’ used by many mocking frameworks.

* patch
  * As a decorator: mock classes or objects in a module
  * As a context manager in a with statement
  * *path.dict*
<pre><code>
>>> foo = {'key': 'value'}
>>> original = foo.copy()
>>> with patch.dict(foo, {'newkey': 'newvalue'}, clear=True):
...     assert foo == {'newkey': 'newvalue'}
...
>>> assert foo == original
</code></pre>
* sentinel
* Mock support the mocking of Python magic methods

---
> The easiest way of using magic methods is with the *MagicMock* class
<pre><code>
>>> from mock import MagicMock
>>> mock = MagicMock()
>>> mock.__str__.return_value = 'foobarbaz'
>>> str(mock)
'foobarbaz'
>>> mock.__str__.assert_called_once_with()
>>> mock = Mock()
>>> mock.__str__ = Mock(return_value = 'wheeeeee')
>>> str(mock)
'wheeeeee'
</code></pre>

* *autospec*, *create_autospec*: Auto-speccing can be done through the autospec argument to patch, or the create_autospec function.
>  Auto-speccing creates mock objects that have the same attributes and methods as the objects they are replacing, and any functions and methods (including constructors) have the same *call signature* as the real object.

---
* [Mock Documentation](http://www.voidspace.org.uk/python/mock/)
* [Quick Guide](http://www.voidspace.org.uk/python/mock/#quick-guide)
* [PyPi - Mock](https://pypi.python.org/pypi/mock)