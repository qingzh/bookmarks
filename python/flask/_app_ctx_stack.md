# Flask Globals 解析

## _app_ctx_stack

源文件位置: flask/globals
```python
from functools import partial
from werkzeug.local import LocalStack, LocalProxy


def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of request context')
    return getattr(top, name)


def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of application context')
    return getattr(top, name)


def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of application context')
    return top.app


# context locals
_request_ctx_stack = LocalStack()
_app_ctx_stack = LocalStack()
current_app = LocalProxy(_find_app)
request = LocalProxy(partial(_lookup_req_object, 'request'))
session = LocalProxy(partial(_lookup_req_object, 'session'))
g = LocalProxy(partial(_lookup_app_object, 'g'))

```

### LocalStack

源文件位置: werkzeug/local.py
```python
class LocalStack(object):

    """This class works similar to a :class:`Local` but keeps a stack
    of objects instead.  This is best explained with an example::

        >>> ls = LocalStack()
        >>> ls.push(42)
        >>> ls.top
        42
        >>> ls.push(23)
        >>> ls.top
        23
        >>> ls.pop()
        23
        >>> ls.top
        42

    They can be force released by using a :class:`LocalManager` or with
    the :func:`release_local` function but the correct way is to pop the
    item from the stack after using.  When the stack is empty it will
    no longer be bound to the current context (and as such released).

    By calling the stack without arguments it returns a proxy that resolves to
    the topmost item on the stack.

    .. versionadded:: 0.6.1
    """

    def __init__(self):
        self._local = Local()

    @property
    def top(self):
        """The topmost item on the stack.  If the stack is empty,
        `None` is returned.
        """
        try:
            return self._local.stack[-1]
        except (AttributeError, IndexError):
            return None
```
