# roles_console
Add / Remove roles to a user from command line

## Flags

* --role    - required, string, role for the user
* --email   - required, string, email of user you wish to change the role of
* --addrole - ADDS the role to specified user
* --remrole - REMOVES the role from a specified user

## Setup

* remove the underscore from _config.ini's name and fill in with valid data.
* Install dependencies (you need pip for that):

```
pip install -r requirements.txt
```

* You might have to run

```
chmod +x AddRole.py
```


## Example

This will grant the role 'superadmin' to user with email address 'test@user.com'

```
./AddRole.py --email test@user.com --role superadmin --addrole True
```

This will remove the role 'superadmin' from user with email address 'test@user.com'

```
./AddRole.py --email test@user.com --role superadmin --remrole True
```
