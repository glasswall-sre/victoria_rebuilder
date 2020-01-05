# destroyer

Allows the creation and DESTRUCTION of SAAS environments.

## Usage

### Prerequisites
- Python 3.7+
- Pip

### Config

#### Access Configuration
```yaml
- ***REMOVED***
    access_token:
  ***REMOVED***
  ***REMOVED***
  ***REMOVED***
```

- `access_token`: The PAT token associated to the email and organisaiton.
- `organisation`: The organisation in Azure DevOps.
- `project`: The project in Azure DevOps
- `email`: The email account associated to the PAT token.

#### Deployment Configuration
```yaml
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
```
- `stage`: Name of the stage. The releases in each stage are all run first before the next stage is complete
- `releases`: List of releases and their name. The name is the name of the release in Azure DevOps

### Help text

```
Usage: victoria destroyer [OPTIONS] COMMAND [ARGS]...

  The Destroyer allows the destruction and rebuilding of environments via
  CLI.

Options:
  -h, --help  Show this message and exit.

Commands:
  copy     CLI call for rebuilding an environment based off another...
  rebuild  CLI call for rebuilding a specific kubernetes environment...

```

### Examples

#### Rebuild an an environment

Rebuild is defined as building up the environment not destroying.

```
victoria destroyer rebuild pent
```

#### Copy an an environment

Copy is defined as building an environment based off the state of the other environment.

```
python destroyer copy qa pent perf
```

Would copy the status of qa to pent and perf

## Development

### Prerequisites
- Python 3.x
- Pipenv

### Quick start
1. Clone this repo.
2. Run `pipenv sync`
3. You're good to go. You can run commands using the package inside a
   `pipenv shell`, and modify the code with your IDE.
