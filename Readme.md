# Terraform and Kubernetes/Helm Management Scripts

This repository contains two Python scripts designed to help automate the management of Terraform configurations and Kubernetes resources, including Helm releases.

## Table of Contents

1. [Terraform Management Script](#terraform-management-script)
    - [Functions](#functions)
2. [Kubernetes and Helm Management Script](#kubernetes-and-helm-management-script)
    - [Functions](#functions-1)
3. [How to Use](#how-to-use)

---

## Terraform Management Script

This script helps manage Terraform configurations, including initialization, planning, applying, destroying, validation, and formatting.

### Functions

- **terraform_init(terraform_dir)**  
  Initializes the Terraform configuration in the specified directory.

- **terraform_plan(terraform_dir, var_file=None)**  
  Runs `terraform plan` to preview changes. Optionally accepts a `.tfvars` file.

- **terraform_apply(terraform_dir, var_file=None, auto_approve=False)**  
  Runs `terraform apply` to apply the changes. Optionally accepts a `.tfvars` file and auto-approve flag.

- **terraform_destroy(terraform_dir, var_file=None, auto_approve=False)**  
  Destroys the Terraform-managed infrastructure. Optionally accepts a `.tfvars` file and auto-approve flag.

- **terraform_validate(terraform_dir)**  
  Validates the Terraform configuration files.

- **terraform_fmt(terraform_dir)**  
  Formats the Terraform configuration files.

### How to Use

1. Run the script and input the path to your Terraform configuration directory.
2. Select the action you want to perform (init, plan, apply, destroy, validate, fmt).
3. Follow the prompts for options like `.tfvars` files or auto-approval.

---

## Kubernetes and Helm Management Script

This script helps manage Kubernetes namespaces and Helm releases. It can create namespaces, list Helm releases, and install, upgrade, rollback, or uninstall Helm charts.

### Functions

- **create_namespace(namespace, kubeconfig_path)**  
  Creates a new Kubernetes namespace if it doesn't already exist.

- **list_releases(namespace)**  
  Lists all Helm releases in the specified namespace.

- **helm_install(release_name, chart, namespace, kubeconfig_path, values_file=None)**  
  Installs a Helm release with the specified chart and optional `values.yaml` file.

- **helm_upgrade(release_name, chart, namespace, kubeconfig_path, values_file=None)**  
  Upgrades an existing Helm release to a new chart version or with a new `values.yaml` file.

- **helm_rollback(release_name, revision, kubeconfig_path, namespace)**  
  Rolls back a Helm release to a specific revision.

- **helm_uninstall(release_name, kubeconfig_path, namespace)**  
  Uninstalls a Helm release from the specified namespace.

### How to Use

1. Run the script and input the Kubernetes namespace and path to your `kubeconfig` file.
2. The script will create the namespace if it doesn't exist and list the Helm releases in that namespace.
3. Select the action to perform (install, upgrade, rollback, uninstall) and provide the necessary information (release name, chart name, etc.).

---

