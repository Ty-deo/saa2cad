print("Please be patient as dialog box should appear soon! - TD")

import os
import tkinter
from tkinter import filedialog, messagebox

"""

Tyler de Jonge, Keller foundations, 2020/2/25
Developed to quickly trim the SAA tool data output into a format that can be read with AutoCAD
TODO: Work with relative path AND absolute path *complete*
TODO: Get file browser working *complete*
TODO: Get it working as executable *complete*
TODO: Get it working to output .scr *complete* WOHO working!!!
2020/3/2 Cleaned up a lot, started using f-strings which make print statements easier to read and less type casting issues

"""

#First read files
stringToMatch = 'Vertex #,' # this string indicates the column header for the start of data. Every line after contains data
lineIndex = 0
startRecord = 0

#Using FileBrowser from tkinter to get input file for manipulation
root = tkinter.Tk()
root.withdraw()
messagebox.showinfo("Select text output from SAA","Please select the .txt output data file from the SAA tool that you would like to transfer into AutoCAD. This program will output the selected filename with an added \"xAutoCADe.txt\" to show it's ready for AutoCAD. Then proceed with the guideline and ascpoint function(or SCRIPT) outlined by Nikko in the word document.")
fileName = filedialog.askopenfilename()						#instead or running program with argument as input, use tkinter and file browser to select file
print(f'File inputted: {fileName}')										
outputPath = os.path.dirname(os.path.abspath(fileName))
print(f'Output directory will be: {outputPath}\n')


#Read out relevant information
# print("Please enter data filepath with extension(Should be txt):", end='')
# fileName = input()
fileNameOut = os.path.splitext(os.path.basename(fileName))
print("fileNameOut: " + str(fileNameOut))
print("Path at terminal when executing this file(current working directory: " + os.getcwd() + "\n")
# with open(fileName, 'r') as input_file:
# 	print("Input file has been received \n***\n")
# 	contents = input_file.read()
# 	print(contents)
# 	print("\n***\nConcluded reading")
# 	input_file.close()


#This section manipulates the data into the .scr format. AutoCAD has built in function SCRIPT that will be able to read this.
with open(fileName, 'r') as input_file2, open(outputPath +'\\' + fileNameOut[0] +'xAutoCADe.scr', 'w') as output_file:
	contentsline = input_file2.readlines()
	for line in contentsline:
		if startRecord == 0:																		#This is so when writing starts the cmd window isn't as flooded
			print("Checking..." + line, end='')
		if stringToMatch in line and startRecord == 0:												#Check for 'Vertex #' start of Data
			startRecord = 1																			#Found start of Data variable
			print ("\nFound line: " + line + "\n***Start recording into output file now***\n.\n.\n.\n", end='')
			output_file.write("OSMODE 0\n3DPOLY ")
		elif startRecord == 1:
			truncLine = line.split(" ", 4)															#stop at 4 because everything after isn't used(AccelerationXYZ and Temp). This probably doesn't save any time but in my head its not worth to split more since we don't use the data.
			#print(truncLine)																		#checking
			#print(f'{truncLine[1]}{truncLine[2]}{truncLine[3][:-1]} ')								
			output_file.write(f'{truncLine[1]}{truncLine[2]}{truncLine[3][:-1]} ')					#Remove the , after Z(mm) because AutoCAD gets confused							
			#print("Appended line " + str(lineIndex))												#check
			lineIndex = lineIndex + 1
	output_file.write('\nOSMODE 1\n')
	print(f'Appended {lineIndex} lines, or {lineIndex} SAA data points')		
	input_file2.close()
	output_file.close()
	print("\nSuccessfully created file: " + outputPath +'\\' + fileNameOut[0] +'xAutoCADe.scr Ready for input to AutoCAD with SCRIPT function(equivalent of ascpoint.lsp). Use word document guideline from Niko\n')
		
"""*How to use input()*
print("Please enter something: ", end='')
answer = input()
print("Your input was: " + answer)"""