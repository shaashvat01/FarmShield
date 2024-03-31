import pandas as pd

# Load the CSV files
train_df = pd.read_csv('/mnt/data/train.csv')
submission_df = pd.read_csv('/mnt/data/sample_submission.csv')

# Display the first few rows of the train dataframe
print(train_df.head())

# Display the first few rows of the sample submission dataframe
print(submission_df.head())
