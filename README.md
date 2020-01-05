# destroyer

Allows the creation and DESTRUCTION of SAAS environments.

## Usage

### Prerequisites
- Python 3.7+
- Pip

### Config

#### Access Configuration
```yaml
- access:
    access_token:
    organisation: glasswall
    project: Glasswall Cloud
    email: apotter-dixon@glasswallsolutions.com
```

- `access_token`: The PAT token associated to the email and organisaiton.
- `organisation`: The organisation in Azure DevOps.
- `project`: The project in Azure DevOps
- `email`: The email account associated to the PAT token.

#### Deployment Configuration
```yaml
deployments:
  - stage: deploy_init_infrastructure
    releases:
      - name: Platform.Infrastructure
  - stage: deploy_kubernetes_infrastructure
    releases:
      - name: Platform.Kubernetes
```
- `stage`: Name of the stage. The releases in each stage are all run first before the next stage is complete
- `releases`: List of releases and their name. The name is the name of the release in Azure DevOps

### Help text

```
Usage: cli.py rebuild [OPTIONS] [CFG]

  CLI call for rebuilding a specific kubernetes environment Arguments:
  cfg (str): Path to the config file.     env (str): Environment to rebuild.

Options:
  --env TEXT  Environment you want to rebuild.  [required]
  --help      Show this message and exit.

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
