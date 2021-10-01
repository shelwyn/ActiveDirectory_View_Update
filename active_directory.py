import ldap
import ldap.filter
from ldap.controls import SimplePagedResultsControl

class active_directory():
    l = ldap.initialize("ldap://XXX.XXX.XXX.XXX")  # AD SERVER IP
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
    bind = l.simple_bind_s("LOGIN_ID", "PASSWORD") # CREDENTIALS
    base = "dc=tbg, dc=GlobalIS, dc=grp"
    page_control = SimplePagedResultsControl(True, size=1000, cookie='')
    def get_ad_users():

        criteria = "(&(objectClass=user)(sAMAccountName=*))"
        attributes = ['cn', 'proxyAddresses', 'distinguishedName', 'displayName', 'company',
                      'sAMAccountName', 'mail', 'sn', 'givenName', 'manager', 'title', 'uid'
            , 'department', 'designation', 'l', 'userPrincipalName', 'extensionAttribute14']
        response = active_directory.l.search_ext(active_directory.base, ldap.SCOPE_SUBTREE, criteria, attributes, serverctrls=[active_directory.page_control])
        result = []
        pages = 0
        item = 0
        while True:
            pages += 1
            rtype, rdata, rmsgid, serverctrls = active_directory.l.result3(response)
            for dn, entry in rdata:
                try:
                    cn = entry['company']
                    mail = entry['mail']
                    dn = entry['distinguishedName']
                    print(mail,cn,dn)
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
            active_directory.page_control.cookie = controls[0].cookie
            response = active_directory.l.search_ext(active_directory.base, ldap.SCOPE_SUBTREE, criteria, attributes, serverctrls=[active_directory.page_control])
        active_directory.l.unbind()


    def update_ad_user():
        dn_to_mod = "CN=Shelwyn Corte,OU=Users,OU=Data Management,DC=xxx,DC=xxx,DC=xxx" #Users DN
        dn_to_mod = dn_to_mod.format(ldap.filter.escape_filter_chars("", 1))
        value_to_replace ="COMPANY_NAME"
        value_to_replace_bytes = str.encode(value_to_replace)
        mod_attrs = [(ldap.MOD_REPLACE, 'company', value_to_replace_bytes)] # Updating the company attribute
        active_directory.l.modify_s(dn_to_mod, mod_attrs)
        active_directory.l.unbind()
        print("User Updated")

main=active_directory
main.get_ad_users()
main.update_ad_user()
