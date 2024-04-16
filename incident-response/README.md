![Cloud Sniper](../images/logo.png "Cloud Sniper")

### AWS Terraform Deployment

<div style="text-align:center"><img src="../images/deployment.png" alt="Cloud Sniper" width=800px/></div>

***Cloud Sniper*** utilizes [Terraform](https://www.terraform.io/) to automate the deployment of its entire infrastructure. Each functionality will be added in Terraform stacks format. A stack takes a holistic approach, avoiding dependencies with other stacks and can be seamlessly integrated into a deployment plan by providing the necessary input variables.


**Requirements:**

1. AWS CLI
2. Programmatic access key or IAM role for AWS
3. Configured AWS local profile
4. Terraform CLI

**Deployment Steps:**

1. Clone the Cloud Sniper repository:
```bash
~$ git clone https://github.com/cloud-sniper/cloud-sniper.git
```

2. Navigate to the desired stack directory:
```bash
~$ cd cloud-sniper/terraform/stacks/[stack-name]
```

3. Set the required environment variables in the `variables.tf` file.
4. Create a `main.tf` file with your credentials or use your IAM role as appropriate:
```hcl
provider "aws" {
  region                    = "your-region"
  shared_credentials_file   = "/your-home/.aws/credentials"
  profile                   = "your-profile"
}
```

5. Initialize Terraform:
```bash
 ~/[stack-name]$ terraform init
```

6. Generate an execution plan:
```bash
~/[stack-name]$ terraform plan
```

7. Apply the Terraform configuration:
```bash
~/[stack-name]$ terraform apply [yes]
```
