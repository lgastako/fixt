from fixt import Environment
from fixt import VarProxy


class TestVarProxy(object):

    def setup_method(self, method):
        self.env = Environment({})

    def test_AS(self):
        x = VarProxy("x", self.env)
        assert str(x.AS("y")) == "x AS y"

    def test_chain(self):
        x = VarProxy("x", self.env)
        assert str(x.y) == "x.y"
