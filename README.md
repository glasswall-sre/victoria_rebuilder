<div align="center" style="text-align:center">

# Victoria Rebuilder

Victoria Rebuilder is a V. I. C. T. O. R. I. A is a plugin that allows you to run multiple Azure DevOps release pipelines 

<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria_rebuilder&metric=alert_status">
<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria_rebuilder&metric=sqale_rating">
<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria_rebuilder&metric=reliability_rating">
<img align="center" src="https://codecov.io/gh/glasswall-sre/victoria_rebuilder/branch/master/graph/badge.svg">
<img align="center" src="https://img.shields.io/github/license/glasswall-sre/victoria_rebuilder">
<img align="center" src="https://github.com/glasswall-sre/victoria_rebuilder/workflows/CI%20Pipeline/badge.svg">

</div>

## Features

* Run a series of release pipelines based on a stages most recent successful releases in Azure DevOps.
* Run a series of release pipelines for a stage based off another stage's most recent successful releases in Azure DevOps.

## Prerequisites

* Python 3.7+
* Pip
* Pipenv

## Installation

``` terminal
pipenv install -U victoria_rebuilder
```

## Usage

### Config

There is an [example configuration](https://github.com/glasswall-sre/victoria_rebuilder/blob/master/example_config.yaml) file provided please update it as you see fit using the guidance below.

#### Access Configuration

``` yaml
access:
  access_token:
  organisation: Organisation
  project: Azure DevOps Project
  email: user@organisation.com
```

* `access_token` : The PAT token associated to the email and organisation. The PAT Token must have Read and Write access to Releases.
* `organisation` : The organisation in Azure DevOps.
* `project` : The project in Azure DevOps
* `email` : The email account associated to the PAT token.

##### Encrypting data for config values

In the config, the `access` section expects data that is encrypted. This can be
achieved with the pre-build `victoria encrypt` command. Details on this
can be found in [the documentation](https://sre.glasswallsolutions.com/victoria/user-guide.html#cloud-encryption):

1. Make sure you've set up your [Victoria cloud encryption backend](https://sre.glasswallsolutions.com/victoria/user-guide.html#azure).
2. Paste the required values (i.e. `access_token`, `organisation`, `project` and `email`) into the following Victoria command like:
   ```
   $ victoria encrypt data <access_token>
   ```
3. The command should output a YAML object containing fields `data`, `iv`, `key` and `version`.
   This is the encrypted value string and can be safely stored in config.
   Put this YAML object into your `access` section like:
   ```yaml
   access:
      access_token:
        data: <snip>
        iv: <snip>
        key: <snip>
        version: <snip>
      organisation:
        data: <snip>
        iv: <snip>
        key: <snip>
        version: <snip>
      project:
        data: <snip>
        iv: <snip>
        key: <snip>
        version: <snip>
      email:
        data: <snip>
        iv: <snip>
        key: <snip>
        version: <snip>
   ```

#### Deployment Configuration

```yaml
deployments:
  stage: deploy_init_infrastructure
    releases:
      - name: Platform.Infrastructure
  stage: deploy_kubernetes_infrastructure
    releases:
      - name: Platform.Kubernetes
```

* `stage` : Name of the stage. The releases in each stage are all run first before the next stage is complete
* `releases` : List of releases and their name. The name is the name of the release in Azure DevOps

### Help text

```terminal
Usage: victoria rebuilder [OPTIONS] COMMAND [ARGS]...

  The rebuilder allows the destruction and rebuilding of environments via
  CLI.

Options:
  -h, --help  Show this message and exit.

Commands:
  copy     CLI call for rebuilding an environment based off another...
  optional flags:
      -r, ---resume     If you want the rebuilder to use the previous state file.

  rebuild  CLI call for rebuilding a specific kubernetes environment...
  optional flags:
      -r, ---resume     If you want the rebuilder to use the previous state file.
      -a, --auto-retry  If a release fails to deploy, instead of prompting the user 
                        for a y/n on retry, it automatically retries the deployment.
```

### CLI Examples

#### Rebuild an environment

Rebuild is defined as running the release pipelines associated with the stage `pent` in this example.

```terminal
victoria rebuilder rebuild pent
```

#### Copy an environment

Copy is defined as running the release for a stage based of an other stage. The use case for this is if you created a new stage and want it to have the same release version as the dev stage.

```terminal
python rebuilder copy qa pent perf
```

Would copy the status of qa to pent and perf

## Contribution

### Bug reports

[You can submit a bug report here.](https://github.com/glasswall-sre/victoria_rebuilder/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D+%7BDescription+of+issue%7D)

### Feature requests

[You can request a new feature here.](https://github.com/glasswall-sre/victoria_rebuilder/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BREQUEST%5D)

### Vulnerability reports

We prefer vulnerabilities to be reported in private so as to minimise their
impact (so we can fix them before they are exploited!). To this end, please
email any security vulnerability reports to '[sre@glasswallsolutions.com](mailto://sre@glasswallsolutions.com)'.
We would appreciate it if you use the issue template in the link below.
All vulnerabilities will be acknowledged within one business day.

[You can publicly report a security vulnerability here.](https://github.com/glasswall-sre/victoria_rebuilder/issues/new?assignees=&labels=Incident%2C+bug&template=vulnerability-report.md&title=%5BVULNERABILITY%5D)

### Pull requests

We accept pull requests! To contribute: 

1. Pick up an unassigned issue from [our issue board](https://github.com/glasswall-sre/victoria_rebuilder/issues).

   Assign yourself to the issue so other people know you're working on it.

2. Work on your code in a feature branch that's got a descriptive name (like `rework-fancy-integrator` ).
3. Follow the [Google style guide for Python](http://google.github.io/styleguide/pyguide.html).

   We use [pylint](https://pypi.org/project/pylint/) to lint our code.
   We run pylint without the 'convention' and 'refactor' message classes.
   You can lint your code with: `pipenv run pylint victoria_destroyer --disable="C,R"` .
   We use [yapf](https://github.com/google/yapf) to automatically format our code. We recommend having it
   format the code whenever you save.

4. Make commits for each part of your pull request. Try not to make too many (if it's a small issue you may only need one).

   We try to use [the imperative mood](https://chris.beams.io/posts/git-commit/#imperative)
   in commit message subjects.

5. We expect all new code to have at least 80% test coverage. This is enforced by [Codecov](https://codecov.io/gh/glasswall-sre/victoria_rebuilder).
06. To run tests locally and check coverage, use: `pipenv run pytest tests/ --cov=victoria_rebuilder` .
07. When ready to merge, create a pull request from your branch into master.
8. Make sure you link your pull request to the issue(s) it addresses.
9. The [CI build](https://github.com/glasswall-sre/victoria_rebuilder/actions?query=workflow%3ACI) will run 

   for your pull request. If it fails then it cannot be merged. Inspect the output, figure
   out why it failed, and fix the problem.
   The CI build will lint your code, run tests, and send coverage/code to Codecov
   and [SonarCloud](https://sonarcloud.io/dashboard?id=victoria_rebuilder). 

11. Someone will review your pull request and suggest changes if necessary.
12. When everything is signed off, your pull request will be merged! Congrats.

## Development

### Prerequisites

* Python 3.x
* Pipenv

### Quick start

01. Clone this repo.
02. Run `pipenv sync`
03. You're good to go. You can run commands using the package inside a

`pipenv shell` , and modify the code with your IDE.

## License 

[Victoria Rebuilder is licensed under the MIT license.](https://github.com/glasswall-sre/victoria_rebuilder/blob/master/LICENSE)
