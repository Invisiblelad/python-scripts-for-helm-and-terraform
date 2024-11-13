import subprocess
import argparse
import os

def terraform_init(terraform_dir):
    """
    Initializes the Terraform configuration in the specified directory.
    
    :param terraform_dir: The directory containing the Terraform configuration.
    """
    try:
        subprocess.run(["terraform", "init"], cwd=terraform_dir, check=True)
        print(f"Terraform initialized in the directory {terraform_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing Terraform: {e}")

def terraform_plan(terraform_dir, var_file=None):
    """
    Runs terraform plan in the specified directory to preview changes.
    
    :param terraform_dir: The directory containing the Terraform configuration.
    :param var_file: Path to a .tfvars file (optional).
    """
    command = ["terraform", "plan"]
    if var_file:
        command.extend(["-var-file", var_file])
    
    try:
        subprocess.run(command, cwd=terraform_dir, check=True)
        print(f"Terraform plan executed in the directory {terraform_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing terraform plan: {e}")
        print("Command that failed:", " ".join(command))

def terraform_apply(terraform_dir, var_file=None, auto_approve=False):
    """
    Runs terraform apply in the specified directory to apply changes.
    
    :param terraform_dir: The directory containing the Terraform configuration.
    :param var_file: Path to a .tfvars file (optional).
    :param auto_approve: Automatically approve the apply (optional).
    """
    command = ["terraform", "apply"]
    if var_file:
        command.extend(["-var-file", var_file])
    if auto_approve:
        command.append("-auto-approve")
    
    try:
        subprocess.run(command, cwd=terraform_dir, check=True)
        print(f"Terraform apply executed in the directory {terraform_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error applying terraform configuration: {e}")

def terraform_destroy(terraform_dir, var_file=None, auto_approve=False):
    """
    Destroys the Terraform-managed infrastructure.
    
    :param terraform_dir: The directory containing the Terraform configuration.
    :param var_file: Path to a .tfvars file (optional).
    :param auto_approve: Automatically approve the destroy (optional).
    """
    command = ["terraform", "destroy"]
    if var_file:
        command.extend(["-var-file", var_file])
    if auto_approve:
        command.append("-auto-approve")
    
    try:
        subprocess.run(command, cwd=terraform_dir, check=True)
        print(f"Terraform destroy executed successfully in '{terraform_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error destroying Terraform infrastructure: {e}")

def terraform_validate(terraform_dir):
    """
    Validates the Terraform configuration files.
    
    :param terraform_dir: The directory containing the Terraform configuration.
    """
    try:
        subprocess.run(["terraform", "validate"], cwd=terraform_dir, check=True)
        print(f"Terraform configuration validated successfully in '{terraform_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error validating Terraform configuration: {e}")

def terraform_fmt(terraform_dir):
    """
    Formats the Terraform configuration files.
    
    :param terraform_dir: The directory containing the Terraform configuration.
    """
    try:
        subprocess.run(["terraform", "fmt"], cwd=terraform_dir, check=True)
        print(f"Terraform configuration files formatted successfully in '{terraform_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting Terraform configuration: {e}")

def main():
    print("Welcome to the Terraform Management Script!")
    
    terraform_dir = input("Enter the path to your Terraform configuration directory: ").strip()
    
    if not os.path.exists(terraform_dir):
        print(f"Error: The directory '{terraform_dir}' does not exist.")
        return
    
    action = input("Please select the action you want to perform (init/plan/apply/destroy/validate/fmt): ").strip().lower()

    if action == "init":
        terraform_init(terraform_dir)
    elif action == "plan":
        var_file = input("Enter the path to a .tfvars file (optional, press Enter to skip): ").strip()
        terraform_plan(terraform_dir, var_file if var_file else None)
    elif action == "apply":
        var_file = input("Enter the path to a .tfvars file (optional, press Enter to skip): ").strip()
        auto_approve = input("Auto-approve changes? (yes/no): ").strip().lower() == 'yes'
        terraform_apply(terraform_dir, var_file if var_file else None, auto_approve)
    elif action == "destroy":
        var_file = input("Enter the path to a .tfvars file (optional, press Enter to skip): ").strip()
        auto_approve = input("Auto-approve destruction? (yes/no): ").strip().lower() == 'yes'
        confirm = input(f"Are you sure you want to destroy resources in '{terraform_dir}'? (y/n): ").strip().lower()
        if confirm == 'y':
            terraform_destroy(terraform_dir, var_file if var_file else None, auto_approve)
        else:
            print("Destroy action aborted.")
    elif action == "validate":
        terraform_validate(terraform_dir)
    elif action == "fmt":
        terraform_fmt(terraform_dir)
    else:
        print(f"Error: Unknown action '{action}'.")

if __name__ == "__main__":
    main()

