# statistical analysis on the created result csv files

import pandas as pd
import matplotlib.pyplot as plt

## Read data_processing_times.csv and data_triples_analysis.csv and combine into one dataframe based on the columns 'Filename' and 'subject'
times_df = pd.read_csv('data_analysis_times.csv')
triples_df = pd.read_csv('data_triples_analysis.csv')

# change the column name 'Filename' to 'subject' in triples_df
triples_df = triples_df.rename(columns={'Filename': 'subject'})

combined_df = pd.merge(times_df, triples_df, on=['subject'])

# cleaning dataset - remove rows with a negative elapsed_time or zero number of triples
combined_df = combined_df[combined_df['elapsed_time'] >= 0]
combined_df = combined_df[combined_df['Number of Triples'] > 0]

# calculate the correlation between the number of triples and the file size
correlation_triples_size = combined_df['Number of Triples'].corr(combined_df['File Size (KB)'])
print(f'Correlation between number of triples and file size: {correlation_triples_size}')

# plot the number of triples vs file size
plt.scatter(combined_df['Number of Triples'], combined_df['File Size (KB)'])
plt.xlabel('Number of Triples')
plt.ylabel('File Size (KB)')
plt.title('File Size vs Number of Triples')
plt.grid()
plt.savefig('file_size_vs_number_of_triples.png')

# clear the plot
plt.clf()

# calculate the correlation between the number of triples and the elapsed time
correlation = combined_df['elapsed_time'].corr(combined_df['Number of Triples'])
print(f'Correlation between number of triples and elapsed time: {correlation}')

# plot the elapsed time vs number of triples
plt.scatter(combined_df['Number of Triples'], combined_df['elapsed_time'])
# plt.xlabel('Number of Triples')
# plt.ylabel('Elapsed Time (seconds)')    
plt.title('Elapsed Time vs Number of Triples')
plt.grid()
plt.savefig('elapsed_time_vs_number_of_triples.png')

# clear the plot
plt.clf()

# calculate the correlation between file size and elapsed time
correlation_size = combined_df['elapsed_time'].corr(combined_df['File Size (KB)'])
print(f'Correlation between file size and elapsed time: {correlation_size}')

# plot the elapsed time vs file size
plt.scatter(combined_df['File Size (KB)'], combined_df['elapsed_time'])
plt.xlabel('File Size (KB)')
plt.ylabel('Elapsed Time (seconds)')    
plt.title('Elapsed Time vs File Size')
plt.grid()
plt.savefig('elapsed_time_vs_file_size.png')

# clear the plot
plt.clf()