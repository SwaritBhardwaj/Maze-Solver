'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:          [ 1032 ]
# Author List:      [ Swarit ]
# Filename:         task_1b.py
# Functions:        applyPerspectiveTransform, detectMaze, writeToCsv, getContour, rearrange, encode_maze
#                   [ Comma separated list of functions in this file ]
# Global variables: width, height, cellSize
#                   [ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################

# Global variables
width,height = 512,512
cellSize = width/10

################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

def getContour(img):

    """
    Purpose:
    ---
    takes a canny image and a maze test case image as input and checks for a 4 corner contour with the maximum area

    Input Arguments:
    ---
    'img', 'original' :   [ numpy array ], [ numpy array ]
            maze image in the form of a numpy array
    
    Returns:
    ---
    `largest` :  [ numpy array ]
            resultant coordinates of maximum area of a 4 cornered contour
    """
        
    maxArea = 0
    largest = []
    
    contours, hrc = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            perimeter = cv2.arcLength(cnt,True)
            points = cv2.approxPolyDP(cnt, 0.005*perimeter, True)
            corners = len(points)
            if corners == 4 and maxArea < area:
                largest = points
                maxArea = area

    return largest

def rearrange(array):

    """
    Purpose:
    ---
    takes an array of length = 4 as input and applies an algorithm to rearrange its items in the format:
            [ [0,0],[width,0],[0,height],[width,height] ]

    Input Arguments:
    ---
    'array':   [ numpy array ]
            corner cordinates of largest 4 corner cotour in the form of a numpy array
    
    Returns:
    ---
    `array_new` :  [ numpy array ]
            resultant coordinates of maximum area of a 4 cornered contour in required sequence
    """

    array = array.reshape((4,2))
    array_new = np.zeros((4,1,2))
    
    add = array.sum(1)                           # THE ORIGIN WILL BE THE MINIMUM SUM (AS IN 0+0) AND THE FARTHEST POINT WILL BE THE MAX(AS IN WIDTH + HEIGHT)
    array_new[0] = array[np.argmin(add)]
    array_new[3] = array[np.argmax(add)]
    
    diff = np.diff(array,1)                      
    array_new[1] = array[np.argmin(diff)]
    array_new[2] = array[np.argmax(diff)]

    return array_new

def encode_maze(img, coordinates):

    """
    Purpose:
    ---
    takes a threshhold warped image of a maze test case image and coordinates of a cell as input and firstly slices the image for extracting
    the cell of given coordinate and then provides it with a cellNumber.

    Input Arguments:
    ---
    'img', 'coordinates' :   [ numpy array ], [ numpy array ]
            maze image and coordinates in the form of a numpy array
    
    Returns:
    ---
    `cellNumber` :  [ integer ]
            resultant encoded cell number based on wall oreintation
    """
    
    cell = []
    
    size = int(cellSize)

    # GIVING THE ORIGIN OF THE CELL AND IT'S WIDTH, HEIGHT
    y0 = size*coordinates[0]
    x0 = size*coordinates[1]
    y  = size*(coordinates[0] + 1)
    x  = size*(coordinates[1] + 1)
    
    cell = img[y0:y, x0:x]

    size = int(cellSize)
    
    NORTH = (not bool((cell[0][int(size/2)])))*(2**1)
    EAST  = (not bool((cell[int(size/2)][size-1])))*(2**2)
    SOUTH = (not bool((cell[size-1][int(size/2)])))*(2**3)
    WEST  = (not bool((cell[int(size/2)][0])))*(2**0)
    
    # THE WARPED IMAGE NOT BEING PERFECT, DEMANDS THE BELOW BLOCK OF CODE SO THAT THE OUTPUT IS ROBUST ON THE SIDES
    
    if y0 == 0:
        NORTH = 2
        if x >= 509:
            EAST  = 2**2
        elif x0 == 0:
            WEST = 1
    elif x0 ==0:
         WEST = 1
         if y >= 509:
             SOUTH = 8
         elif y0 == 0:
             NORTH = 2
    elif x >= 509:
          EAST  = 2**2
          if y0 == 0:
              NORTH = 2
          elif y >= 509:
             SOUTH = 8
    elif y >= 509:
           SOUTH = 8
           if x0 == 0:
               WEST = 1
           elif x >= 509:
               EAST  = 2**2    
    
    cellNumber = NORTH + EAST + SOUTH + WEST
    
    return cellNumber

    
##############################################################


def applyPerspectiveTransform(input_img):

        """
        Purpose:
        ---
        takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

        Input Arguments:
        ---
        `input_img` :   [ numpy array ]
                maze image in the form of a numpy array
        
        Returns:
        ---
        `warped_img` :  [ numpy array ]
                resultant warped maze image after applying Perspective Transform
        
        Example call:
        ---
        warped_img = applyPerspectiveTransform(input_img)
        """

        warped_img = None

        ##############  ADD YOUR CODE HERE  ##############

        # PREPROCESSING THE IMAGE        
        imgBlur = cv2.GaussianBlur(input_img, (7,7), 1)
        ret,thresh1 = cv2.threshold(imgBlur, 80, 200,cv2.THRESH_BINARY)
        imgCanny = cv2.Canny(thresh1, 50,50)
        kernel = np.ones((4,4))
        imgDial = cv2.dilate(imgCanny,kernel,iterations = 2)
        imgThresh = cv2.erode(imgDial, kernel, iterations = 1)
        
        # GETTING THE CORNER POINTS OF THE MAZE, AND THEN RE-ARRANGING THEM
        largest = getContour(imgThresh)
        largest_rearranged = rearrange(largest)

        # GETTING THE REQUIRED WARP
        pts1 = np.float32(largest_rearranged)        
        pts2 = np.float32( [ [0,0],[width,0],[0,height],[width,height] ] )
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        warped_img = cv2.warpPerspective(input_img, matrix, (width,height))
        
        ##################################################

        return warped_img


def detectMaze(warped_img):

        """
        Purpose:
        ---
        takes the warped maze image as input and returns the maze encoded in form of a 2D array

        Input Arguments:
        ---
        `warped_img` :    [ numpy array ]
                resultant warped maze image after applying Perspective Transform
        
        Returns:
        ---
        `maze_array` :    [ nested list of lists ]
                encoded maze in the form of a 2D array

        Example call:
        ---
        maze_array = detectMaze(warped_img)
        """

        maze_array = []

        ##############  ADD YOUR CODE HERE  ##############

        # PREPROCESSING THE WARPED IMAGE
        gray_image = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
        _,warpedThresh = cv2.threshold(gray_image, 137, 180,cv2.THRESH_BINARY)

        # GETTING THE ENCODED CELL NUMBER AND STORING IT IN THE LIST
        for i in range(0,10):
            maze_array.append([])
            for j in range(0,10):
                coordinates = [i,j]
                cellNumber = encode_maze(warpedThresh, coordinates)
                maze_array[i].append(cellNumber)

        ##################################################
                
        return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

	# path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'csv/' + 'maze0' + str(file_num) + '.csv'
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()
	
	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):
			
			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'csv/' + 'maze0' + str(file_num) + '.csv'
			
			# read the image file
			input_img = cv2.imread(img_file_path)

			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)

				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')
					
					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)

					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				
				else:

					print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()
			
			else:

				print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')

