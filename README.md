# Clover Health Assignment Libert Pierrick

Requires Python 3.9+ and PostgreSQL 14+

## Install

To install all dependencies:

```bash
make install
```

To delete all dependencies:

```bash
make clean
```

## Launch

### Basic Mode

You can launch the programm by running this command:

```bash
make launch
```

### Dry Mode

But you may also want to launch in dry mode with this command:

```bash
make launch_dry
```

You'll be able to see the different errors you may have and the SQL requests which would be run in basic mode.

## Test

You can test the code by launching this command:

```bash
make test
```

## Code linting

```bash
make lint
```

In order to enforce a certain code quality, [pylint](https://pypi.org/project/pylint/) with the option `--fail-under` is used, and is configured to fail if the score is below 9.0 (see Makefile).

Before each Pull Request, we expect developers to run this command and fix most of errors or warnings displayed.

After creating a new module, it has to be added into the Makefile command.

## Environment variables

| Name                          | Type    | Default                                      | Description                                                                                      |
| ----------------------------- | ------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| POSTGRESQL_ADDON_DB           | String  | base                                         | Name of the psql database                                                                   |
| POSTGRESQL_ADDON_USER         | String  | base                                         | Name of the psql user                                                                       |
| POSTGRESQL_ADDON_PASSWORD     | String  | base                                         | Password of the psql user                                                                       |
| POSTGRESQL_ADDON_HOST         | String  | localhost                                    | Domain/Ip of the psql database                                                                   |
| POSTGRESQL_ADDON_PORT         | Integer | 5432                                         | Port of the psql database                                                                   |
