# Implementation Plan - Ultra-Simple POC

- [ ] 1. Set up minimal Terraform project
  - Create single main.tf file with all resources
  - Configure AWS provider with basic settings
  - Use local state file for simplicity
  - _Requirements: 4.3, 5.1_

- [ ] 2. Create basic VPC and networking
  - Create VPC with single public and private subnet in one AZ
  - Set up Internet Gateway and route table
  - Create security groups for ALB and ECS (allow HTTP) and RDS (allow PostgreSQL from ECS)
  - _Requirements: 3.1, 3.2_

- [ ] 3. Set up minimal RDS database
  - Create RDS PostgreSQL db.t4g.micro instance in private subnet
  - Enable PostGIS extension in user data or init script
  - Use minimal storage (20GB gp2) and 1-day backup retention
  - _Requirements: 1.2, 8.1_

- [ ] 4. Create ECS infrastructure
  - Set up ECR repository for Django Docker images
  - Create ECS cluster with Fargate launch type
  - Define task definition for Django app (0.25 vCPU, 512 MB RAM)
  - Create ECS service with single task, no auto-scaling
  - _Requirements: 4.1, 4.2, 1.1_

- [ ] 5. Set up Application Load Balancer
  - Create ALB in public subnet with HTTP listener
  - Configure target group pointing to ECS service
  - Set up basic health checks on Django health endpoint
  - _Requirements: 2.2, 2.4_

- [ ] 6. Create IAM roles
  - Create ECS task execution role with ECR and CloudWatch permissions
  - Create ECS task role with RDS access permissions
  - _Requirements: 3.5_

- [ ] 7. Set up GitHub Actions deployment
  - Create workflow to build Django Docker image
  - Configure ECR push and ECS service update
  - Use GitHub secrets for AWS access key and secret key
  - _Requirements: 7.1, 7.2, 7.3_