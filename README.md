# Hybrid Spotify Recommendation System  
A scalable recommendation system combining collaborative and content-based filtering, deployed on AWS

## 🛠️ Tech Stack  
- **Data & Pipeline**: DVC, AWS S3  
- **CI/CD**: GitHub Actions, Docker, AWS ECR, CodeDeploy  
- **Deployment**: AWS EC2/ECS, Auto Scaling Groups (Blue/Green)  
- **Frameworks**: Streamlit (for UI), Scikit-Learn (ML)

## 📊 System Overview

### Image 1: Machine Learning Workflow with Version Control
![Machine Learning Workflow](docs/ml_workflow.png)
- Illustrates a pipeline for developing and versioning a machine learning model.
- Includes Notebook, Source Code, and Data managed with Git and DVC.
- Uses GitHub for code storage and AWS S3 for large datasets/models.
- Features a DVC pipeline (`dvc.yaml`) to automate and reproduce the best model.

### Image 2: CI/CD and Deployment Process
![CI/CD and Deployment Process](docs/architecture.png)
- Depicts the CI/CD pipeline and deployment to production.
- Automates builds with GitHub Actions and Docker, storing images in AWS ECR.
- Packages artifacts and stores them in AWS S3.
- Deploys using AWS CodeDeploy with Blue/Green strategy for zero-downtime updates.

### CI/CD Pipeline
```mermaid
graph LR
  A[GitHub Actions] --> B[Build Docker Image]
  B --> C[Push to ECR]
  C --> D[Deploy via CodeDeploy]


