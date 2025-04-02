$$ Step 1: Compute Cosine Similarity

Cosine similarity between vectors A and B is calculated as:
cos(θ)=A⋅B∥A∥∥B∥=∑i=1nAiBi∑i=1nAi2∑i=1nBi2
cos(θ)=∥A∥∥B∥A⋅B​=∑i=1n​Ai2​
​∑i=1n​Bi2​
​∑i=1n​Ai​Bi​​

Calculations for x3 vs others:
Pair	Dot Product	‖x3‖	‖x‖	Cosine Similarity
x3·x1	(4×1)+(1×2)+(2×3) = 12	√(4²+1²+2²) = √21 ≈ 4.58	√(1²+2²+3²) = √14 ≈ 3.74	12 / (4.58 × 3.74) ≈ 0.79
x3·x2	(4×3)+(1×1)+(2×3) = 19	√21 ≈ 4.58	√(3²+1²+3²) = √19 ≈ 4.36	19 / (4.58 × 4.36) ≈ 0.94
x3·x4	(4×3)+(1×5)+(2×6) = 29	√21 ≈ 4.58	√(3²+5²+6²) = √70 ≈ 8.37	29 / (4.58 × 8.37) ≈ 0.83
x3·x5	(4×5)+(1×6)+(2×9) = 44	√21 ≈ 4.58	√(5²+6²+9²) = √142 ≈ 11.92	44 / (4.58 × 11.92) ≈ 0.85
Step 2: Sort and Recommend

Ranked by similarity to x3:

    x2 (Song B): 0.94

    x5 (Song D): 0.85

    x4 (Song C): 0.83

    x1 (Song A): 0.79

Final Recommendation

For a user who listens to Song x3, recommend:

    Song B (x2), 2. Song D (x5), 3. Song C (x4)
