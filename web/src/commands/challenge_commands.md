# Challenge CLI documentation

#### Import

```shell
$ flask challenge import --all
$ flask challenge import --challenge CHALLENGE_NAME
```

To reimport a challenge, you can add `--force`.

#### List

```shell
$ flask challenge list
```

#### Randomly create challenges

```shell
$ flask challenge create -n NUMBER
# NUMBER: how many challenges should be created
```

#### Deletion

```shell
$ flask challenge delete --all
$ flask challenge delete --challenge CHALLENGE_NAME
```

#### Check

```shell
$ flask challenge check --all
$ flask challenge check --challenge CHALLENGE_NAME
```

#### Build

```shell
$ flask challenge build --all
$ flask challenge build --challenge CHALLENGE_NAME
```
