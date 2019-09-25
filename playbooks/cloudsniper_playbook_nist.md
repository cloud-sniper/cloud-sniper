# Cloud Sniper Playbook - NIST approach

1.  Asset Management
    
    <details>
            <summary>ID.AM</summary>
    The data, personnel, devices, systems, and facilities that enable the organization to achieve business purposes are identified and managed consistent with their relative importance to business objectives and the organization’s risk strategy
    </details>

    1.  **IAM**
        
        1.  Checks whether IAM groups have at least one IAM user
            **#IDENTIFY**            

        2.  Checks whether IAM users are members of at least one IAM group
            **#IDENTIFY**
        
        3.  Checks that none of the IAM users have policies attached. IAM users must inherit permissions from IAM groups or roles
            **#IDENTIFY**

        4.  Checks whether your Identity and IAM users have passwords or active access keys that have not been used within the specified number of days you provided
            **#IDENTIFY**

    2.  **Security groups**
    
        1.  Checks that the default security group of any VPC does not allow inbound or outbound traffic
            **#IDENTIFY**

    2.  **ACM Certificates**
    
        1.  Checks whether ACM Certificates in your account are marked for expiration within the specified number of days
            **#IDENTIFY**

    3.  **KMS**

        1.  Checks whether the active access keys are rotated within the number of days specified in maxAccessKeyAge
            **#IDENTIFY**

    4.  **CloudTrail**

        1.  Checks whether CloudTrail is enabled in your account
            **#IDENTIFY**

        2. Checks whether CloudTrail trails are configured to send logs to CloudWatch logs
            **#IDENTIFY**

        3. Checks whether CloudTrail is configured to use the server side encryption (SSE-KMS)
            **#IDENTIFY**

        4. Checks whether CloudTrail creates a signed digest file with logs
            **#IDENTIFY**

        5. Checks that there is at least one multi-region CloudTrail
            **#IDENTIFY**

    5.  **GuardDuty**

        1.  Checks whether GuardDuty is enabled in your account and region
            **#IDENTIFY**



 