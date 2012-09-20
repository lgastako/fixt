from fixt import INSERT
from fixt import SELECT
from fixt import users
from fixt import username
from fixt import u

from fixtcommontests import FixtCommonTests


class TestExplicitInvocation(FixtCommonTests):

    def insert_to_users(self):
        return (INSERT(users,
                       username='lgastako',
                       pw_hash=self.EX_PW_HASH))

    def select_from_users_with_aliases(self):
        # Note we avoided having to explicitly import the pw_hash alias
        # by explicitly importing the u alias and then using that.  Obviously
        # this is more important when there are more attributes in the
        # projection.

        y = u.pw_hash
        assert str(y) == "u.pw_hash"
        x = y.AS('bcrypt_pw')
        assert str(x) == "u.pw_hash AS bcrypt_pw"
        sel = SELECT(username, x)
        fro = sel.FROM(users.AS('u'))
        return fro
