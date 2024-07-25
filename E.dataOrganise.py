import os
import shutil

# Define the directories
dataSplitDir = './C.split/'
noisyDir = './D.noisy/'
organisedDir = './E.organised/'
noiseStds = [5, 10, 15, 20, 25, 30]

# Ensure the organised directory exists
os.makedirs(organisedDir, exist_ok=True)
organisedTrainDir = os.path.join(organisedDir, 'train')
organisedTestDir = os.path.join(organisedDir, 'test')
organisedValidationDir = os.path.join(organisedDir, 'validation')
organisedNoisyTrainDir = os.path.join(organisedDir, 'noisyTrain')
organisedNoisyTestDir = os.path.join(organisedDir, 'noisyTest')
organisedNoisyValidationDir = os.path.join(organisedDir, 'noisyValidation')

# Create subdirectories in the organised folder
os.makedirs(organisedTrainDir, exist_ok=True)
os.makedirs(organisedTestDir, exist_ok=True)
os.makedirs(organisedValidationDir, exist_ok=True)
os.makedirs(organisedNoisyTrainDir, exist_ok=True)
os.makedirs(organisedNoisyTestDir, exist_ok=True)
os.makedirs(organisedNoisyValidationDir, exist_ok=True)

def copyRename(srcDir, dstDir, prefix):
    for file in os.listdir(srcDir):
        if file.endswith('.nii.gz'):
            srcFilePath = os.path.join(srcDir, file)
            dstFilePath = os.path.join(dstDir, f'{prefix}_{file}')
            shutil.copy(srcFilePath, dstFilePath)

# Process the train, test and validation files
for prefix in noiseStds:
    # Train files
    trainSrcDir = os.path.join(dataSplitDir, 'train')
    copyRename(trainSrcDir, organisedTrainDir, prefix)
    
    # Test files
    testSrcDir = os.path.join(dataSplitDir, 'test')
    copyRename(testSrcDir, organisedTestDir, prefix)
    
    # Validation files
    validationSrcDir = os.path.join(dataSplitDir, 'validation')
    copyRename(validationSrcDir, organisedValidationDir, prefix)

# Aggregate noisy files
def aggregateNoisy(srcDir, dstDir):
    for root, dirs, files in os.walk(srcDir):
        for file in files:
            if file.endswith('.nii.gz'):
                srcFilePath = os.path.join(root, file)
                dstFilePath = os.path.join(dstDir, file)
                shutil.copy(srcFilePath, dstFilePath)

for noiseStd in noiseStds:
    noisySubDir = f'noisy{noiseStd}'
    noisyTrainSrcDir = os.path.join(noisyDir, noisySubDir, 'noisyTrain')
    noisyTestSrcDir = os.path.join(noisyDir, noisySubDir, 'noisyTest')
    noisyValidationSrcDir = os.path.join(noisyDir, noisySubDir, 'noisyValidation')
    
    # Aggregate files into organised noisyTrain, noisyTest and noisyTest folders
    aggregateNoisy(noisyTrainSrcDir, organisedNoisyTrainDir)
    aggregateNoisy(noisyTestSrcDir, organisedNoisyTestDir)
    aggregateNoisy(noisyValidationSrcDir, organisedNoisyValidationDir)

print("Organisation Complete.")
