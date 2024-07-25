import os
import shutil

# Define the source directory and the target directory
sourceDir = './simulation_images4Kofi/'
targetDir = './A.extracted/'

# Create the target directory if it doesn't exist
os.makedirs(targetDir, exist_ok=True)

# Iterate over each subdirectory in the source directory
for folder in os.listdir(sourceDir):
    folderPath = os.path.join(sourceDir, folder)
    
    # Check if it's a directory
    if os.path.isdir(folderPath):
        # Iterate over each sub-subdirectory (healthy, RMCAo, LMCAo)
        for subfolder in ['healthy', 'LMCAo', 'RMCAo']:
            subfolderPath = os.path.join(folderPath, subfolder)
            # Define the source file path
            sourceFile = os.path.join(subfolderPath, 'perfusion_0.5x0.5x3.0.nii.gz')
            # Check if the file exists
            if os.path.exists(sourceFile):
                # Define the target file name
                targetFileName = f'{folder}_{subfolder}_perfusion_0.5x0.5x3.0.nii.gz'
                targetFile = os.path.join(targetDir, targetFileName)
                # Copy the file to the target directory
                shutil.copy2(sourceFile, targetFile)
                print(f'Copied {sourceFile} to {targetFile}')
            else:
                print(f'File {sourceFile} does not exist')

print('Files Extracted Successfully.')
