import ldap
from ldap.controls import SimplePagedResultsControl

class active_directory():
    def get_ad_users():
        l = ldap.initialize("ldap://XXX.XXX.XXX.XXX")  # AD SERVER IP
        l.protocol_version = ldap.VERSION3
        l.set_option(ldap.OPT_REFERRALS, 0)
        bind = l.simple_bind_s("LOGIN_ID", "PASSWORD") # CREDENTIALS
        page_control = SimplePagedResultsControl(True, size=1000, cookie='')
        base = "dc=tbg, dc=GlobalIS, dc=grp"
        criteria = "(&(objectClass=user)(sAMAccountName=*))"
        attributes = ['cn', 'proxyAddresses', 'distinguishedName', 'displayName', 'company',
                      'sAMAccountName', 'mail', 'sn', 'givenName', 'manager', 'title', 'uid'
            , 'department', 'designation', 'l', 'userPrincipalName', 'extensionAttribute14']
        response = l.search_ext(base, ldap.SCOPE_SUBTREE, criteria, attributes, serverctrls=[page_control])
        result = []
        pages = 0
        item = 0
        while True:
            pages += 1
            rtype, rdata, rmsgid, serverctrls = l.result3(response)
            for dn, entry in rdata:
                try:
                    cn = entry['cn']
                    cn = str(cn).replace("[b'", "").replace("']", "")
                    print(cn)
                except:
                    pass

                item += 1

            result.extend(rdata)
            controls = [control for control in serverctrls
                        if control.controlType == SimplePagedResultsControl.controlType]
            if not controls:
                print('The server ignores RFC 2696 control')
                break
            if not controls[0].cookie:
                break
            page_control.cookie = controls[0].cookie
            response = l.search_ext(base, ldap.SCOPE_SUBTREE, criteria, attributes, serverctrls=[page_control])
        l.unbind()

main=active_directory
main.get_ad_users()
