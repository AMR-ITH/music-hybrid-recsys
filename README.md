# Hybrid Spotify Recommendation System  
A scalable recommendation system combining collaborative and content-based filtering, deployed on AWS

## 🛠️ Tech Stack  
- **Data & Pipeline**: DVC, AWS S3  
- **CI/CD**: GitHub Actions, Docker, AWS ECR, CodeDeploy  
- **Deployment**: AWS EC2/ECS, Auto Scaling Groups (Blue/Green)  
- **Frameworks**: Streamlit (for UI), Scikit-Learn (ML)

## 📊 System Overview

### Architecture
First Diagram: Machine Learning Workflow with Version Control
![Hybrid Recommender Architecture](docs/ml_workflow)

### CI/CD Pipeline
```mermaid
graph LR
  A[GitHub Actions] --> B[Build Docker Image]
  B --> C[Push to ECR]
  C --> D[Deploy via CodeDeploy]


