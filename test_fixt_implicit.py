import fixt as _

from fixtcommontests import FixtCommonTests


class TestImplicitInvocation(FixtCommonTests):
    EX_PW_HASH = ('$2a$12$/lAOMdKlTaqZuiK5D8oPfuz'
                  'l1WFwPFrxxXLYk9IAAfRs75dU1y/Y.')

    def test_insert_to_users(self):
        q = _.INSERT(_.users,
                        username='lgastako',
                        pw_hash=self.EX_PW_HASH)

        assert str(q) in (("INSERT INTO users (username, pw_hash)\n"
                           "VALUES (%(username)X, %(pw_hash)X)"),
                          ("INSERT INTO users (pw_hash, username)\n"
                           "VALUES (%(pw_hash)X, %(username)X)"))

    def test_select_from_users_with_aliases(self):
        # Note we could just use _.pw_hash here, but we use the u alias
        # to preserve parity with the explicit case.

        q = (_.SELECT(_.username, _.u.pw_hash.AS('bcrypt_pw'))
                .FROM(_.users.AS('u')))

        assert str(q) == ("SELECT username, u.pw_hash AS bcrypt_pw\n"
                          "FROM users AS u")
