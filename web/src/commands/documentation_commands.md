# Documentation CLI documentation

#### Import

```shell
$ flask documentation import --all
$ flask documentation import --documentation DOCUMENTATION_NAME
```

To reimport a documentation, you can add `--force`.

#### List

```shell
$ flask documentation list
```

#### Randomly create documentation

```shell
$ flask documentation create -n NUMBER
# NUMBER: how many documentations should be created
```

#### Deletion

```shell
$ flask documentation delete --all
$ flask documentation delete --documentation DOCUMENTATION_NAME
```

#### Check

```shell
$ flask documentation check --all
$ flask documentation check --documentation DOCUMENTATION_NAME
```

#### Build

```shell
$ flask documentation build --all
$ flask documentation build --documentation DOCUMENTATION_NAME
```
