from fixt import INSERT
from fixt import SELECT
from fixt import users
from fixt import username
from fixt import u

from fixtcommontests import FixtCommonTests


class TestExplicitInvocation(FixtCommonTests):
    EX_PW_HASH = ('$2a$12$/lAOMdKlTaqZuiK5D8oPfuz'
                  'l1WFwPFrxxXLYk9IAAfRs75dU1y/Y.')

    def test_insert_to_users(self):
        q = (INSERT(users,
                    username='lgastako',
                    pw_hash=self.EX_PW_HASH))

        exq1 = ("INSERT INTO users (username, pw_hash)\n"
                "VALUES (%(username)X, %(pw_hash)X)")
        exq2 = ("INSERT INTO users (pw_hash, username)\n"
                "VALUES (%(pw_hash)X, %(username)X)")
        assert str(q) in (exq1, exq2)

    def test_select_from_users_with_aliases(self):
        # Note we avoided having to explicitly import the pw_hash alias
        # by explicitly importing the u alias and then using that.  Obviously
        # this is more important when there are more attributes in the
        # projection.

        q = (SELECT(username, u.pw_hash.AS('bcrypt_pw'))
             .FROM(users.AS('u')))

        assert str(q) == ("SELECT username, u.pw_hash AS bcrypt_pw\n"
                          "FROM users AS u")
