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
