import sys
import platform

from types import ModuleType


if "windows" in platform.system().lower():
    raise ImportError("fixt is currently only supported on linux and osx.")


def sql_list(*args):
    return ", ".join(map(str, args))


class FROM(object):

    def __init__(self, prefix, *args):
        self.prefix = prefix
        self.from_clause = sql_list(*args)

    def __str__(self):
        return "%s\nFROM %s" % (self.prefix, self.from_clause)


class SELECT(object):

    def __init__(self, *args):
        attr_name_list = sql_list(*args)
        self.sql = "SELECT %s" % attr_name_list

    def __str__(self):
        return self.sql

    def FROM(self, *args):
        return FROM(str(self), *args)


class INSERT(object):

    def __init__(self, table_name, **binds):
        attr_nvps = [(name, value) for name, value in binds.iteritems()]
        attr_name_list = ", ".join(n for n, _ in attr_nvps)
        attr_value_fmt = ", ".join("%%(%s)X" % attr_name
                                   for attr_name, _
                                   in attr_nvps)
        self.sql = "INSERT INTO %s (%s)\nVALUES (%s)" % (
            str(table_name), attr_name_list, attr_value_fmt)

    def __str__(self):
        return self.sql


class ASProxy(object):

    def __init__(self, expr, alias, missing_source):
        self.expr = expr
        self.alias = alias
        self.missing_source = missing_source

    def __str__(self):
        return "%s AS %s" % (self.expr, self.alias)


class VarProxy(object):

    def __init__(self, name, missing_source, prefix=""):
        self.name = name
        self.missing_source = missing_source
        self.prefix = prefix

    def __str__(self):
        res = self.name
        if self.prefix:
            res = "%s.%s" % (self.prefix, res)
        return res

    def AS(self, alias):
        return ASProxy(self.name, alias, self.missing_source)
    as_ = AS

    def __getattr__(self, key):
        new_prefix = self.name
        if self.prefix:
            new_prefix = self.prefix + "." + new_prefix
        proxy = VarProxy(key, self.missing_source, new_prefix)
        if key == "pw_hash":
            import ipdb; ipdb.set_trace()
        return proxy

    def __missing__(self, key):
        return self.missing_source.__missing__(key)


class Environment(dict):

    def __init__(self, *args, **kwargs):
        super(Environment, self).__init__(*args, **kwargs)
        self.setdefault("INSERT", INSERT)

    def __missing__(self, key):
        if key == "__all__":
            raise ImportError("Please don't use import * - either import fixed (perhaps as _) or import specific things from it.")
        if key.startswith("__"):
            raise KeyError(key)
        if key not in self:
            self[key] = self.make_proxy(key)
        return self[key]

    def make_proxy(self, key):
        return VarProxy(key, self)


# INSERT(users,
#     username='lgastako',
#     pw_hash='$2a$12$/lAOMdKlTaqZuiK5D8oPfuzl1WFwPFrxxXLYk9IAAfRs75dU1y/Y.'
# )


# lifted from https://github.com/amoffat/sh/blob/master/sh.py
# this is a thin wrapper around THIS module (we patch sys.modules[__name__]).
# this is in the case that the user does a "from sh import whatever"
# in other words, they only want to import certain programs, not the whole
# system PATH worth of commands.  in this case, we just proxy the
# import lookup to our Environment class
class SelfWrapper(ModuleType):

    def __init__(self, self_module):
        # this is super ugly to have to copy attributes like this,
        # but it seems to be the only way to make reload() behave
        # nicely.  if i make these attributes dynamic lookups in
        # __getattr__, reload sometimes chokes in weird ways...
        for attr in ["__builtins__", "__doc__", "__name__", "__package__"]:
            setattr(self, attr, getattr(self_module, attr))

        self.self_module = self_module
        # self.env = Environment(globals())
        self.env = Environment({
            "INSERT": INSERT,
            "SELECT": SELECT,
            "VarProxy": VarProxy,
            "Environment": Environment
        })

    def __getattr__(self, name):
        return self.env[name]


if __name__ == "__main__":
    # do we care?
    pass
else:
    # we're being imported from somewhere
    self = sys.modules[__name__]
    sys.modules[__name__] = SelfWrapper(self)
