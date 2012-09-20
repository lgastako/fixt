import fixt as _

from fixtcommontests import FixtCommonTests


class TestImplicitInvocation(FixtCommonTests):

    def insert_to_users(self):
        return _.INSERT(_.users,
                        username='lgastako',
                        pw_hash=self.EX_PW_HASH)

    def select_from_users_with_aliases(self):
        # Note we could just use _.pw_hash here, but we use the u alias
        # to preserve compatability with the explicit case.
        sel = _.SELECT(_.username, _.u.pw_hash.AS('bcrypt_pw'))
        fro = sel.FROM(_.users.AS('u'))
        return fro
