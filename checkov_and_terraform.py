import os
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr.decode('utf-8')}")
    return result.stdout.decode('utf-8')

def install_checkov():
    try:
        run_command("checkov --version")
    except Exception:
        run_command("pip install checkov")

def run_checkov():
    install_checkov()
    try:
        run_command("checkov -d . --policy-directory custom_policies")
        return True
    except Exception as e:
        print(f"Checkov failed: {e}")
        return False

def run_terraform_commands():
    run_command("terraform init")
    run_command("terraform plan -out=plan.out")
    run_command("terraform show -json plan.out > plan.json")

if __name__ == "__main__":
    checkov_passed = run_checkov()
    run_terraform_commands()
    if checkov_passed:
        print("Checkov passed. Team members can apply the Terraform plan manually.")
    else:
        print("Checkov issues found, not applying Terraform.")
