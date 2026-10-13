# JobMatch ML

Machine learning project that predicts how well a job advertisement matches a candidate skills and experience.

## Project Goal

Build an end-to-end machine learning application that analyses job advertisements and produces a job suitability score.

## Technology

- Python
- pandas
- NumPy
- scikit-learn
- Natural Language Processing (NLP)
- Machine Learning
- AWS

## Current Status

### Phase 1 - Project Setup

- [x] Project directory created
- [x] Python virtual environment created
- [x] Python 3.14.3 configured
- [x] pandas installed
- [x] NumPy installed
- [x] scikit-learn installed
- [x] matplotlib installed
- [x] Jupyter installed
- [x] Initial jobs.csv dataset created
- [x] Dataset successfully loaded with pandas

### Initial Dataset

The initial development dataset contains 12 job advertisements.

The current match field is:

- 1 = good match
- 0 = poor match

This dataset is for development and learning only. It will be expanded before the model is considered meaningful.

## Planned Machine Learning Pipeline

Job Advertisement
        |
        v
Text Processing
        |
        v
TF-IDF
        |
        v
ML Classifier
        |
        v
Match Probability
        |
        v
Job Match Score
        |
        v
Web Dashboard
        |
        v
AWS

## Planned AWS Components

Potential AWS services include:

- Amazon S3
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon CloudFront

AWS deployment will come after the local machine-learning model is working.

## Development Approach

1. Create and understand the dataset
2. Clean and prepare the data
3. Convert job text into numerical features
4. Train a baseline ML model
5. Evaluate the model
6. Test predictions on unseen jobs
7. Improve the dataset and model
8. Build an API
9. Deploy components to AWS
10. Create a portfolio dashboard

## Important Principle

This project aims to demonstrate genuine machine learning rather than simply calling an external AI API.

The model will be trained and evaluated using a labelled dataset, with appropriate evaluation metrics.

## Project Location

C:\Users\Administrator\job-match-ml



## Model Evaluation

JobMatch ML uses a TF-IDF text vectorisation and Logistic Regression pipeline to estimate how closely a job advert matches a candidate profile.

### Five-Fold Cross-Validation Results

The model was evaluated using stratified five-fold cross-validation on a dataset of 52 job examples.

| Metric | Mean Score |
|---|---:|
| Accuracy | 92.36% |
| Precision | 94.29% |
| Recall | 92.00% |
| F1-score | 91.67% |

### Evaluation Approach

Stratified five-fold cross-validation divides the dataset into five folds while maintaining a similar proportion of each class. The model is trained and evaluated across the folds to provide a broader assessment than a single train/test split.

The final model is then trained on all 52 available examples and saved to `models/jobmatch_model.joblib` for use by the prediction script and Flask web application.

### Limitations

- The dataset contains only 52 manually assembled job examples.
- Cross-validation results may not represent performance on real-world job adverts.
- The variation in fold accuracy indicates that performance depends on which examples are held out for testing.
- The model's predicted scores are not calibrated probabilities of securing a job.
- A larger, more diverse dataset and further testing on genuinely unseen job adverts are needed before drawing strong conclusions about reliability.

These results are preliminary and are intended to demonstrate the model evaluation process in a portfolio project, rather than establish production-level performance.



### Application Testing

The trained model was tested through both the command-line prediction script and the Flask web application.

**Test 1: Unrelated job role**

- Job title: Marketing Executive
- Final match score: 31.70%
- Result: POOR MATCH
- Outcome: The system identified missing marketing-related skills and recommended prioritising other roles.

**Test 2: Relevant cloud support role**

- Job title: Junior AWS Cloud Support Engineer
- Final match score: 84.79%
- Result: EXCELLENT MATCH
- ML relevance: 81.59%
- Skill compatibility: 80.00%
- Experience fit: 100%
- Matched skills: AWS, Linux, Networking and Troubleshooting
- Missing skill: CloudWatch
- Outcome: The system recommended applying for the role.

Both tests completed successfully. The results demonstrate that the application can load the trained model, calculate a combined match score, identify matched and missing skills, and generate a recommendation.

These are functional tests using two example adverts, not proof of general predictive accuracy. The scoring system is a prototype and requires broader testing with unseen, real-world job adverts.

## Functional Testing

The JobMatch ML web application was tested against seven job descriptions covering relevant target roles, a senior cloud position, and unrelated careers.

| Job title | Score | Result |
|---|---:|---|
| Senior AWS Cloud Engineer | 44.08% | Poor Match |
| Retail Store Manager | 29.11% | Poor Match |
| Junior IT Support Technician | 77.27% | Excellent Match |
| Junior Cloud Support Engineer | 84.74% | Excellent Match |
| Junior DevOps Engineer | 75.61% | Excellent Match |
| Junior AWS Cloud Engineer | 67.09% | Good Match |
| Junior Data Analyst | 37.15% | Poor Match |

### Findings

- The application identified relevant junior IT, cloud support, and DevOps roles as promising matches.
- It gave lower scores to the unrelated retail and data analyst roles.
- The senior cloud role received a lower score, reflecting the experience and skills gaps in the test profile.
- The results demonstrate that the application and scoring pipeline work across several different job descriptions.

### Limitations

These seven examples were deliberately selected and do not establish general predictive accuracy. The training dataset is small, skill matching is based on simple text matching, and the final score is a suitability heuristic rather than a probability of being hired. Further testing with a larger, independent dataset would be required to assess real-world performance.


