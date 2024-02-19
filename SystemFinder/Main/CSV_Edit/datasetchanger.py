import pandas as pd
import numpy as np

# Define the lists of graphics cards and CPUs for different file sizes
lower_range_gpus = [
    "NVIDIA GeForce GTX 1050", "NVIDIA GeForce GTX 1660 Ti", "NVIDIA GeForce GTX 1080",
    "NVIDIA GeForce GTX 1080 Ti"
]

higher_range_gpus = [
    "NVIDIA GeForce RTX 2060", "NVIDIA GeForce RTX 2080",
    "NVIDIA GeForce RTX 2080 Ti",
]

lower_range_cpus = [

    "Intel Core i3 12100", "Intel Core i3 12300", "Intel Core i5 10600K",
    "Intel Core i5 11600K", "Intel Core i5 12600K"
]

higher_range_cpus = [
    "Intel Core i5 12400F", "Intel Core i5 13400F", "Intel Core i7 10700K",
    "Intel Core i7 12700K", "Intel Core i9 10900K", "Intel Core i9 12900K",
    "AMD Ryzen 5 7500F", "AMD Ryzen 5 5600X", "AMD Ryzen 7 3700X",
    "AMD Ryzen 7 5800X", "AMD Ryzen 9 3900X", "AMD Ryzen 9 5900X"
]

def parse_file_size(file_size):
    if 'GB' in file_size:
        return float(file_size.replace('GB', '').strip()) * 1024
    elif 'MB' in file_size:
        return float(file_size.replace('MB', '').strip())
    else:
        return 0

def assign_hardware_based_on_size(row):
    file_size_mb = parse_file_size(row['File Size:'])
    if file_size_mb < 25600:  # Less than 25 GB
        row['Graphics Card:'] = np.random.choice(lower_range_gpus)
        row['CPU:'] = np.random.choice(lower_range_cpus)
    else:  # 25 GB or more
        row['Graphics Card:'] = np.random.choice(higher_range_gpus)
        row['CPU:'] = np.random.choice(higher_range_cpus)
    return row

# Sample usage
# Load your CSV file
games_data = pd.read_csv('/Users/murathankarasu/PycharmProjects/SystemFinder/Main/CSV_Edit/games1.csv')

# Apply the function to update hardware based on file size
games_data = games_data.apply(assign_hardware_based_on_size, axis=1)

# Replace all "-" characters with space
games_data = games_data.replace('-', ' ', regex=True)

# Save the updated dataframe
games_data.to_csv('games.csv', index=False)
