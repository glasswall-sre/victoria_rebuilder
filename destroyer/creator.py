from release import Release


def create_environment(environment, access, deployments):
    """
    Initial wrapper to initiate the creation of an environment.

    Arguments:
        environment: The environment to create the deployment on.

    """

    for deployment in deployments:
        run_deployment(deployment, environment, access)
        print(deployment)


def run_deployment(deployment, environment, access):
    """
    Runs the deployment by getting the latest release for each pipeline
    and then running it. 

    """

    releases = []

    deployment_complete = False

    print(deployment.pipelines)

    for pipeline in deployment.pipelines:
        print(pipeline)
        release = Release(pipeline, environment, access)
        releases.append(release)

