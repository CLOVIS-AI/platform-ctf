# Instance CLI

#### List instances

```shell
$ flask instance list
```

#### Check

```shell
# Check for inconsistencies
# For example, instances that are running but not marked in the database
$ flask instance check --inconsistency

# Check for expired instances
$ flask instance check --expired

# Run both checks
$ flask instance check --inconsistency --expired
```

#### Clean

```shell
# Stop all inconsistent instances
$ flask instance clean --inconsistency

# Stop all expired instances
$ flask instance clean --expired

# Stop all inconsistent and expired instances
$ flask instance clean --inconsistency --expired
```
