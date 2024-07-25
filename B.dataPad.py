import os
import nibabel as nib
import numpy as np

# Define the extracted directory and the padded directory
extractedDir = './A.extracted/'
paddedDir = './B.padded/'

# Create the padded directory if it does not exist
os.makedirs(paddedDir, exist_ok=True)

# Function to pad an image to the target shape
def padImage(image, targetShape):
    currentShape = image.shape
    padding = []
    for i in range(len(currentShape)):
        totalPadding = targetShape[i] - currentShape[i]
        padBefore = totalPadding // 2
        padAfter = totalPadding - padBefore
        padding.append((padBefore, padAfter))
    paddedImage = np.pad(image, padding, mode='constant', constant_values=-1024.0)
    return paddedImage

# Find the maximum dimensions
maxDimensions = [0, 0, 0]

for file in os.listdir(extractedDir):
    if file.endswith('.nii.gz'):
        filePath = os.path.join(extractedDir, file)
        img = nib.load(filePath)
        imgData = img.get_fdata()
        shape = imgData.shape
        maxDimensions = [max(maxDimensions[i], shape[i]) for i in range(3)]

print(f"Maximum dimensions: {maxDimensions}")

# Pad images to the maximum dimensions and save them in the padded directory
for file in os.listdir(extractedDir):
    if file.endswith('.nii.gz'):
        filePath = os.path.join(extractedDir, file)
        img = nib.load(filePath)
        imgData = img.get_fdata()
        paddedData = padImage(imgData, maxDimensions)
        
        # Create a new Nifti1Image
        paddedImg = nib.Nifti1Image(paddedData, img.affine)
        
        # Save the padded image in the padded directory
        paddedFilePath = os.path.join(paddedDir, file)
        nib.save(paddedImg, paddedFilePath)
        # print(f"Padded {file} to {maxDimensions} and saved to {paddedFilePath}")

print("Padding Complete.")
