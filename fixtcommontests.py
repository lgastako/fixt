class FixtCommonTests(object):
    EX_PW_HASH = ('$2a$12$/lAOMdKlTaqZuiK5D8oPfuz'
                  'l1WFwPFrxxXLYk9IAAfRs75dU1y/Y.')

    def test_insert_to_users(self):
        q = self.insert_to_users()
        assert str(q) in (("INSERT INTO users (username, pw_hash)\n"
                           "VALUES (%(username)X, %(pw_hash)X)"),
                          ("INSERT INTO users (pw_hash, username)\n"
                           "VALUES (%(pw_hash)X, %(username)X)"))

    def test_select_from_users_with_aliases(self):
        q = self.select_from_users_with_aliases()
        assert str(q) == ("SELECT username, u.pw_hash AS bcrypt_pw\n"
                          "FROM users AS u")
