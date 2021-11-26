# User CLI

#### List users

```shell
$ flask user list
```

#### Create a new user

```shell
# Create a randomly-generated user
$ flask user create --random -n NUMBER
# NUMBER: the number of randomly-generated users to create

# Create a user
$ flask user create OPTIONS
# OPTIONS:
# --admin             Create an administrator
# --username NAME
# --email    EMAIL
# --password PASSWORD
```

#### Deletion

```shell
$ flask user delete --all
$ flask user delete USER_ID
```

#### Administrators

```shell
$ flask user admin --promote USER_ID
$ flask user admin --revoke USER_ID
```
