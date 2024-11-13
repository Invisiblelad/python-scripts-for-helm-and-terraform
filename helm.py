from kubernetes import client, config
import subprocess
import argparse


def create_namespace(namespace, kubeconfig_path):
    """
    Creates a new Kubernetes namespace if it doesn't exist, based on user confirmation.
    
    :param namespace: The name of the Kubernetes namespace to create.
    :param kubeconfig_path: Path to the kubeconfig file.
    """
    config.load_kube_config(config_file=kubeconfig_path)
    v1 = client.CoreV1Api()
    try:
        v1.read_namespace(namespace)
        print(f"Namespace '{namespace}' already exists.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            user_input = input(f"Namespace '{namespace}' does not exist. Would you like to create it? (yes/no): ").strip().lower()
            if user_input == 'yes':
                print(f"Creating namespace '{namespace}'...")
                namespace_metadata = client.V1ObjectMeta(name=namespace)
                namespace_body = client.V1Namespace(metadata=namespace_metadata)
                v1.create_namespace(namespace_body)
                print(f"Namespace '{namespace}' created successfully.")
            else:
                print(f"Skipping the creation of the namespace '{namespace}'.")
        else:
            print(f"Error checking namespace: {e}")


def list_releases(namespace):
    """
    Lists all the Helm releases in the specified namespace.
    
    :param namespace: The Kubernetes namespace to list releases from.
    """
    helm_command = ["microk8s", "helm", "list", "--namespace", namespace]
    try:
        result = subprocess.run(helm_command, capture_output=True, check=True, text=True)
        print(f"Helm releases in namespace '{namespace}':\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error listing Helm releases: {e}")


def helm_install(release_name, chart, namespace, kubeconfig_path, values_file=None):
    """
    Installs a Helm release with a specified chart and optional values.yaml file.
    
    :param release_name: Name of the Helm release.
    :param chart: The Helm chart to install.
    :param namespace: The Kubernetes namespace to install the release in.
    :param values_file: Path to a custom values.yaml file (optional).
    :param kubeconfig: Path to the kubeconfig file 
    """
    config.load_kube_config(config_file=kubeconfig_path)
    helm_command = [
        "microk8s", "helm", "install", release_name, chart, "--namespace", namespace
    ]

    if values_file:
        helm_command.extend(["-f", values_file])

    try:
        subprocess.run(helm_command, check=True)
        print(f"Helm chart '{chart}' deployed as release '{release_name}' in namespace '{namespace}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying Helm chart: {e}")


def helm_upgrade(release_name, chart, namespace, kubeconfig_path, values_file=None):
    """
    Upgrades an existing Helm release to a new chart version or with a new values.yaml file.
    
    :param release_name: Name of the Helm release.
    :param chart: The Helm chart to upgrade to (chart version can be specified).
    :param namespace: The Kubernetes namespace of the Helm release.
    :param values_file: Path to a custom values.yaml file (optional).
    :param kubeconfig: Path to the kubeconfig file . 
    """
    config.load_kube_config(config_file=kubeconfig_path)
    helm_command = [
        "microk8s", "helm", "upgrade", release_name, chart, "--namespace", namespace
    ]
    
    if values_file:
        helm_command.extend(["-f", values_file])
    
    try:
        subprocess.run(helm_command, check=True)
        print(f"Helm chart release {release_name} upgraded to {chart} in namespace {namespace}.")
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading helm chart: {e}")


def helm_rollback(release_name, revision, kubeconfig_path, namespace):
    """
    Rolls back a Helm release to a specific revision.
    
    :param release_name: Name of the Helm release.
    :param revision: The revision number to roll back to.
    :param namespace: The Kubernetes namespace of the Helm release.
    :param kubeconfig: Path to the kubeconfig file.
    """
    config.load_kube_config(config_file=kubeconfig_path)
    helm_command = [
        "microk8s", "helm", "rollback", release_name, str(revision), "--namespace", namespace
    ]

    try:
        subprocess.run(helm_command, check=True)
        print(f"Helm chart rolled back to revision {revision} in namespace {namespace}.")
    except subprocess.CalledProcessError as e:
        print(f"Error rolling back helm chart: {e}")

def helm_uninstall(release_name, kubeconfig_path, namespace):
    """
    Uninstalls (deletes) a Helm release.
    
    :param release_name: Name of the Helm release.
    :param namespace: The Kubernetes namespace of the Helm release.
    :param kubeconfig: Path to the kubeconfig file.
    """
    config.load_kube_config(config_file=kubeconfig_path)
    helm_command = [
        "microk8s", "helm", "uninstall", release_name, "--namespace", namespace
    ]

    try:
        subprocess.run(helm_command, check=True)
        print(f"Helm chart '{release_name}' uninstalled from namespace '{namespace}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error uninstalling helm chart: {e}")


def main():
    print("Welcome to the Helm Release Management Script!")
    
    namespace = input("Enter the Kubernetes namespace: ").strip()
    kubeconfig = input("Enter the path to your kubeconfig file: ").strip()
    create_namespace(namespace, kubeconfig)
    list_releases(namespace)
    release_name = input("Enter the release name: ").strip()
    action = input("Please select the action you want to perform (install/upgrade/rollback): ").strip().lower()

    if action == "install":
        chart = input("Enter the chart name: ").strip()
        values_file = input("Enter the path to a values.yaml file (optional, press Enter to skip): ").strip()
        helm_install(
            release_name,
            chart,
            namespace,
            kubeconfig,
            values_file if values_file else None
        )
    elif action == "upgrade":
        chart = input("Enter the chart name (with version, if necessary): ").strip()
        values_file = input("Enter the path to a values.yaml file (optional, press Enter to skip): ").strip()
        helm_upgrade(
            release_name,
            chart,
            namespace,
            kubeconfig,
            values_file if values_file else None
        )
    elif action == "rollback":
        revision = input("Enter the revision number to roll back to: ").strip()
        if not revision.isdigit():
            print("Error: Please enter a valid number for the revision.")
            return
        helm_rollback(
            release_name,
            int(revision),
            kubeconfig,
            namespace
        )
    elif action == "uninstall":
        confirm = input(f"Are you sure you want to uninstall the release '{release_name}' from the namespace '{namespace}'? (y/n): ").strip().lower()
        if confirm == 'y':
            helm_uninstall(release_name, kubeconfig, namespace)
        else:
            print("Uninstall aborted.")
    else:
        print(f"Error: Unknown action '{action}'.")

if __name__ == "__main__":
    main()


