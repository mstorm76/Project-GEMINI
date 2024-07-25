import os
import shutil
import random

# Define the source and target directories
sourceDir = './B.padded/'
targetDir = './C.split/'

# Create the target directory and subdirectories
os.makedirs(os.path.join(targetDir, 'train'), exist_ok=True)
os.makedirs(os.path.join(targetDir, 'test'), exist_ok=True)
os.makedirs(os.path.join(targetDir, 'validation'), exist_ok=True)

# Function to distribute files into train, test, and validation folders
def distributeFiles(files, trainDir, testDir, valDir):
    random.shuffle(files)
    trainSplit = int(0.85 * len(files))
    testSplit = int(0.05 * len(files)) + trainSplit
    
    trainFiles = files[:trainSplit]
    testFiles = files[trainSplit:testSplit]
    valFiles = files[testSplit:]
    
    for file in trainFiles:
        shutil.copy2(file, trainDir)
    for file in testFiles:
        shutil.copy2(file, testDir)
    for file in valFiles:
        shutil.copy2(file, valDir)

# Collect files based on categories
categories = ['healthy', 'RMCAo', 'LMCAo']
filesByCategory = {category: [] for category in categories}

for file in os.listdir(sourceDir):
    if file.endswith('.nii.gz'):
        for category in categories:
            if category in file:
                filesByCategory[category].append(os.path.join(sourceDir, file))
                break

# Distribute files for each category
for category in categories:
    distributeFiles(
        filesByCategory[category],
        os.path.join(targetDir, 'train'),
        os.path.join(targetDir, 'test'),
        os.path.join(targetDir, 'validation')
    )

print("Files Distributed Successfully.")
