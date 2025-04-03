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


## 🔍 Technical Implementation
### Content-Based Filtering
Below is an example of a content-based filtering recommendation system using cosine similarity to recommend songs based on a target song.

#### Example Data
- `x1 = [1, 2, 3]` (Song A)
- `x2 = [3, 1, 3]` (Song B)
- `x3 = [4, 1, 2]` (Selected Song - Target)
- `x4 = [3, 5, 6]` (Song C)
- `x5 = [5, 6, 9]` (Song D)

#### Step 1: Compute Cosine Similarity
Cosine similarity between vectors \( A \) and \( B \) is calculated as:

\[ \cos(\theta) = \frac{A \cdot B}{|A| |B|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}} \]

**Calculations for `x3` vs others:**

| Pair   | Dot Product               | ‖x3‖       | ‖x‖        | Cosine Similarity       |
|--------|---------------------------|------------|------------|-------------------------|
| x3·x1  | (4×1)+(1×2)+(2×3) = 12   | √21 ≈ 4.58 | √14 ≈ 3.74 | 12 / (4.58 × 3.74) ≈ 0.79 |
| x3·x2  | (4×3)+(1×1)+(2×3) = 19   | √21 ≈ 4.58 | √19 ≈ 4.36 | 19 / (4.58 × 4.36) ≈ 0.94 |
| x3·x4  | (4×3)+(1×5)+(2×6) = 29   | √21 ≈ 4.58 | √70 ≈ 8.37 | 29 / (4.58 × 8.37) ≈ 0.83 |
| x3·x5  | (4×5)+(1×6)+(2×9) = 44   | √21 ≈ 4.58 | √142 ≈ 11.92 | 44 / (4.58 × 11.92) ≈ 0.85 |

#### Step 2: Sort and Recommend
Ranked by similarity to `x3`:
- `x2` (Song B): 0.94
- `x5` (Song D): 0.85
- `x4` (Song C): 0.83
- `x1` (Song A): 0.79

#### Final Recommendation
For a user who listens to Song `x3`, recommend:
1. Song B (`x2`)
2. Song D (`x5`)
3. Song C (`x4`)



