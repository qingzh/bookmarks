flask template

我们先看一下 render_template 的源码
```python
def render_template(template_name_or_list, **context):
    """Renders a template from the template folder with the given
    context."""
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    return _render(ctx.app.jinja_env.get_or_select_template(template_name_or_list),
                   context, ctx.app)
```

调用关系是:
```
flask.templating.render_template 
           ||
    flask.template._render
           ||
    Environment.get_template
           ||
  Environment.loader.get_source
```

再来查看核心文件 flask/templating.py
```python
def _render(template, context, app):
    """Renders the template and fires the signal"""
    rv = template.render(context)
    template_rendered.send(app, template=template, context=context)
    return rv
```
这里渲染的核心是 template 对象，以及 render_template中的
```python
ctx.app.jinja_env.get_or_select_template(template_name_or_list)
```

我们来查看和 render_tempalte 相关的属性:
```python
>>> app.jinja_env
<flask.templating.Environment object at 0x7fc92a21cc10>

>>> app.jinja_env.loader
<flask.templating.DispatchingJinjaLoader object at 0x7fc92a21cf10>

>>> app.jinja_loader
<jinja2.loaders.FileSystemLoader object at 0x7fc92a21cf90>

>>> app.jinja_loader.searchpath
['/home/smalarm/flaskweb/AlarmWeb/templates']

>>> app.jinja_options
ImmutableDict({'extensions': ['jinja2.ext.autoescape', 'jinja2.ext.with_']})
```

##### Jinja Environment

源代码解析
1. 使用 app.create_global_jinja_loader 初始化 template loader
```python
# flask/templating.py
class Environment(jinja2.Environment)
```
借用jinja2的描述:
> The core component of Jinja is the `Environment`.  It contains
    important shared variables like configuration, filters, tests,
    globals and others. 

2. 这里获取对象的方法是 jinja2 原生方法 get_or_select_template
```python
# jinja2/environment.py
    @internalcode
    def get_or_select_template(self, template_name_or_list,
                               parent=None, globals=None):
        if isinstance(template_name_or_list, string_types):
            return self.get_template(template_name_or_list, parent, globals)
        elif isinstance(template_name_or_list, Template):
            return template_name_or_list
        return self.select_template(template_name_or_list, parent, globals)

```

3. 通过字符串获取 template 是使用 Environment.get_template 方法
```python
# jinja2/environment.py
    def get_template(self, name, parent=None, globals=None):
        """Load a template from the loader.  If a loader is configured this
        method ask the loader for the template and returns a :class:`Template`.
        If the `parent` parameter is not `None`, :meth:`join_path` is called
        to get the real template name before loading.

        The `globals` parameter can be used to provide template wide globals.
        These variables are available in the context at render time.

        If the template does not exist a :exc:`TemplateNotFound` exception is
        raised.

        .. versionchanged:: 2.4
           If `name` is a :class:`Template` object it is returned from the
           function unchanged.
        """
        if isinstance(name, Template):
            return name
        if parent is not None:
            name = self.join_path(name, parent)
        return self._load_template(name, self.make_globals(globals))
```
实质是调用 Environment._load_template 方法
```python
    def _load_template(self, name, globals):
        if self.loader is None:
            raise TypeError('no loader for this environment specified')
        try:
            # use abs path for cache key
            cache_key = self.loader.get_source(self, name)[1]
        except RuntimeError:
            # if loader does not implement get_source()
            cache_key = None
        # if template is not file, use name for cache key
        if cache_key is None:
            cache_key = name
        if self.cache is not None:
            template = self.cache.get(cache_key)
            if template is not None and (not self.auto_reload or
                                         template.is_up_to_date):
                return template
        template = self.loader.load(self, name, globals)
        if self.cache is not None:
            self.cache[cache_key] = template
        return template
```

所以获取 Template 的核心方法是 jinja_loader.get_source

##### Jinja2 Loader

flask 自定义了一个 template loader 
```python
# flask/templating.py :: DispatchingJinjaLoader
    def get_source(self, environment, template):
        for loader, local_name in self._iter_loaders(template):
            try:
                return loader.get_source(environment, local_name)
            except TemplateNotFound:
                pass

        raise TemplateNotFound(template)

    def _iter_loaders(self, template):
        loader = self.app.jinja_loader
        if loader is not None:
            yield loader, template

        # old style module based loaders in case we are dealing with a
        # blueprint that is an old style module
        try:
            module, local_name = posixpath.normpath(template).split('/', 1)
            blueprint = self.app.blueprints[module]
            if blueprint_is_module(blueprint):
                loader = blueprint.jinja_loader
                if loader is not None:
                    yield loader, local_name
        except (ValueError, KeyError):
            pass

        for blueprint in itervalues(self.app.blueprints):
            if blueprint_is_module(blueprint):
                continue
            loader = blueprint.jinja_loader
            if loader is not None:
                yield loader, template
```
