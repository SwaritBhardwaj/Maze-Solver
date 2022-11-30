'''
*****************************************************************************************
*
*                       ===============================================
*                       Nirikshak Bot (NB) Theme (eYRC 2020-21)
*                       ===============================================
*
*  This script is to implement Task 4A of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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

####################### IMPORT MODULES #######################

import numpy as np
import cv2
import os
import traceback
import sys
import json


# Import 'maze_processsor.py' file as module
try:
        import maze_processsor

except ImportError:
        print('\n[ERROR] maze_processsor.py file is not present in the current directory.')
        print('Your current directory is: ', os.getcwd())
        print('Make sure maze_processsor.py is present in this current directory.\n')
        sys.exit()
                
except Exception as e:
        print('Your maze_processsor.py throwed an Exception, kindly debug your code!\n')
        traceback.print_exc(file=sys.stdout)
        sys.exit()

##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
#-------------------------------------------------------------------------------
def removeItems(list1, i, j):
        for x in range(i,j+1):
                list1.pop(x)
        return list1

def searchParent(lista, start):
        list1 = []
        current = lista[0]
        for i in range(len(lista)-1):
                if current.parent == lista[i+1]:
                        list1.append(tuple(current.position))
                        current = lista[i+1]
        list1.append(start)                
        return list1[::-1]

class Find_subsets(object):
        
   def subsets(self, nums):
           
      temp_result = []
      self.subsets_util(nums,[0 for i in range(len(nums))],temp_result,0)
      main_result = []
      for lists in temp_result:
         temp = []
         for i in range(len(lists)):
            if lists[i] == 1:
               temp.append(nums[i])
         main_result.append(temp)
      print(main_result)
      return main_result

   def subsets_util(self,nums,temp,result,index):
           
      if index == len(nums):
         result.append([i for i in temp])
         return
      temp[index] = 0
      self.subsets_util(nums,temp,result,index+1)
      temp[index] = 1
      self.subsets_util(nums, temp, result,index + 1)
      

class Find_neighbours(object):
        wall_set = [1,2,4,8]
        Fs =  Find_subsets()
        subsets = Fs.subsets(wall_set)
        def neighbours(self, num, present_coord):
                for Set in self.subsets:
                        if num == sum(Set):
                                self.return_coord = []
                                for item in Set:
                                        if item == 1:
                                                self.return_coord.append([present_coord[0], present_coord[1]-1])
                                        if item == 2:
                                                self.return_coord.append([present_coord[0]-1, present_coord[1]])
                                        if item == 4:
                                                self.return_coord.append([present_coord[0], present_coord[1]+1])
                                        if item == 8:
                                                self.return_coord.append([present_coord[0]+1, present_coord[1]])       
                                return self.return_coord
                                       

#-------------------------------------------------------------------------------

class Node(object):
        g = 0
        h = 0
        f = 0
        def __init__(self, coordinate, parent, parent_g, goal, cost, method):

                # POSITION
                self.position = coordinate

                # PARENT
                self.parent = parent
                # NAVIGATION COST
                self.g = parent_g + cost

                # HEURISTIC COST
                if method == 0:
                        self.h = (goal[0] - coordinate[0]) + (goal[1] - coordinate[1])
                if method == 1:
                        self.h = ((goal[0] - coordinate[0])**2 + (goal[1] - coordinate[1])**2)
                        
                # TOTAL COST        
                self.f = self.g + self.h

                # RETURNING TOTAL COST AND NEW PARENT'S G 
                #return self.f, self.g
                
x = []
def Astar(neighbour_array, parent_node, visited):
        
        global non_visit
        current_iterations = 0
        max_iterations = 10**10
        currentNode = neighbour_array[0]
        currentIndex = 0
        index_visited = 0
        while len(neighbour_array)>0:
                for index, neighbour in enumerate(neighbour_array):                              
                                if neighbour.f < currentNode.f:
                                        currentNode = neighbour
                                        currentIndex = index
                visited.append(currentNode)
                neighbour_array.pop(currentIndex)
                return visited, neighbour_array
         
                
##############################################################


def find_path(maze_array, start_coord, end_coord):
        """
        Purpose:
        ---
        Takes a maze array as input and calculates the path between the
        start coordinates and end coordinates.

        Input Arguments:
        ---
        `maze_array` :   [ nested list of lists ]
                encoded maze in the form of a 2D array

        `start_coord` : [ tuple ]
                start coordinates of the path

        `end_coord` : [ tuple ]
                end coordinates of the path
        
        Returns:
        ---
        `path` :  [ list of tuples ]
                path between start and end coordinates
        
        Example call:
        ---
        path = find_path(maze_array, start_coord, end_coord)
        """

        path = None

        ################# ADD YOUR CODE HERE #################
        path = []
        parent_g = 0
        visited_list = []
        yet_to_visit_list = []
        last_position = start_coord
        c = 1
        # GETTING START AND END
        start_encoded = maze_array[int(start_coord[0])][ int(start_coord[1])]
        current_encoded = start_encoded
        parent_instance = Node(last_position, None, parent_g, end_coord, cost = 0, method = 1)
        visited_list.append(parent_instance)
        
        # FINDING NEIGHBOURS
        if len(visited_list)>0 :
                while c ==1:
                        Fs = Find_neighbours()
                        neighbour_coord = Fs.neighbours(15-current_encoded, last_position)           # neighbours located
                        childrenInsList = []
                        
                        # FINDING TOTAL COST
                        for coord in neighbour_coord:

                                if len([list(visited_child.position) for visited_child in visited_list if list(visited_child.position) == list(coord)]) > 0:
                                        continue
                                
                                Neighbour_instance = Node(coord, visited_list[-1], parent_g, end_coord, cost = 1, method = 1)
                                
                                
                                if len([list(i.g) for i in yet_to_visit_list if list(Neighbour_instance.position) == list(i.position) and list(Neighbour_instance.g) > list(i.g)])>0:
                                        continue
                                yet_to_visit_list.append(Neighbour_instance)
                                
                        if len(yet_to_visit_list) == 0:
                                  path = None
                                  return path
                        # A STAR ALGORITHM
                        visited_list, yet_to_visit_list = Astar(yet_to_visit_list, parent_instance, visited_list)
                        
                        parent_g = visited_list[-1].g
                        
                        current_encoded = maze_array[(visited_list[-1]).position[0]][(visited_list[-1]).position[1]]
                        last_position =   visited_list[-1].position
                        parent_instance = visited_list[-1]
                        
                        if last_position == list(end_coord):
                                c = 0
                        # APPENDING THE CELL COORD IN PATH
                        #  path.append(tuple(last_position))
                        #  print(last_position, parent_g)
                        #  print(path)
        ######################################################
        visited_coords = []
        for i in visited_list:
                visited_coords.append(i.position)                
        new_list = []

        occurence = visited_coords.count(end_coord)
        for index in range(len(visited_list[::-1])-1,-1,-1):
                if visited_list[index].position == list(end_coord):
                        x = searchParent(visited_list[index::-1], start_coord)
                        new_list.append(x)
                                
        if len(new_list) > 1:
                current = new_list[0]
                for i in new_list:
                        
                        if len(i) < len(current):
                                current = i
        else:
                path = new_list[0]          
                
        return path


def read_start_end_coordinates(file_name, maze_name):
        """
        Purpose:
        ---
        Reads the corresponding start and end coordinates for each maze image
        from the specified JSON file
        
        Input Arguments:
        ---
        `file_name` :   [ str ]
                name of JSON file

        `maze_name` : [ str ]
                specify the maze image for which the start and end coordinates are to be returned.

        Returns:
        ---
        `start_coord` : [ tuple ]
                start coordinates for the maze image

        `end_coord` : [ tuple ]
                end coordinates for the maze image
        
        Example call:
        ---
        start, end = read_start_end_coordinates("start_end_coordinates.json", "maze00")
        """

        start_coord = None
        end_coord = None

        ################# ADD YOUR CODE HERE #################
        with open(file_name) as f:
                data = json.load(f)
        path = data[maze_name]

        start_coord = tuple(path["start_coord"])
        end_coord = tuple(path["end_coord"])
        ######################################################

        return start_coord, end_coord

def display_path(frame, path, img_name):
        """
        Purpose:
        ---
        Displays the path by drawing lines on the warped image 
        
        Input Arguments:
        ---
        `frame` :   [ numpy array ]
                warped image
        `path` :  [ list of tuples ]
                        path between start and end coordinates
        `img_name` : [ str ]
                specify the maze image for which the path is to be displayed.
                
        Returns:
        ---
        NA
        
        Example call:
        ---
        display_path(warped_img, path, "maze00")
        """
        start_absolute = (path[0][1]*51 + 25, path[0][0]*51 +25)
        stop_absolute = (path[-1][1]*51 + 25, path[-1][0]*51 +25)

        # DRAWING LINES FOR PATH VISUALIZATION
        for i in range(1, len(path)):
                start_coord = (path[i-1][1]*51 + 25, path[i-1][0]*51 +25)
                end_coord   = (path[i][1]*51 +25, path[i][0]*51 +25)
                frame = cv2.line(frame, start_coord, end_coord, (255,0,0), 4)

        # DRAWING CIRCLES AS REPRESENTATIONS OF START AND END POSITION
        cv2.circle(frame, start_absolute, 0, (0,255,0), 12) # start => green
        cv2.circle(frame, stop_absolute, 0, (0,0,255), 12)  # end   => red 
        cv2.imshow("output_"+maze_name, frame)
        while True:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        cv2.destroyAllWindows()
        
        

# NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
#                                       as input and reads the corresponding start and end coordinates for this image from 'start_end_coordinates.json'
#                                       file by calling read_start_end_coordinates function. It then applies Perspective Transform
#                                       by calling applyPerspectiveTransform function, encodes the maze input in form of 2D array
#                                       by calling detectMaze function and finds the path between start, end coordinates by calling
#                                       find_path function. It then asks the user whether to repeat the same on all maze images
#                                       present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
#                                       read_start_end_coordinates and find_path functions.
if __name__ == "__main__":

        # path directory of images in 'test_cases' folder
        img_dir_path = 'test_cases/'

        file_num = 0

        maze_name = 'maze0' + str(file_num)

        # path to 'maze00.jpg' image file
        img_file_path = img_dir_path + maze_name + '.jpg'

        # read start and end coordinates from json file
        start_coord, end_coord = read_start_end_coordinates("start_end_coordinates.json", maze_name)

        print('\n============================================')
        print('\nFor maze0' + str(file_num) + '.jpg')
        
        # read the 'maze00.jpg' image file
        input_img = cv2.imread(img_file_path)

        # get the resultant warped maze image after applying Perspective Transform
        warped_img = maze_processsor.applyPerspectiveTransform(input_img)

        if type(warped_img) is np.ndarray:

                # get the encoded maze in the form of a 2D array
                maze_array = maze_processsor.detectMaze(warped_img)

                if (type(maze_array) is list) and (len(maze_array) == 10):

                        print('\nEncoded Maze Array = %s' % (maze_array))
                        print('\n============================================')

                        path = find_path(maze_array, start_coord, end_coord)

                        if (type(path) is list):

                                print('\nPath calculated between %s and %s is %s' % (start_coord, end_coord, path))
                                print('\n============================================')
                                display_path(warped_img, path, maze_name)
                        else:
                                print('\n Path does not exist between %s and %s' %(start_coord, end_coord))
                
                else:
                        print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                        exit()
        
        else:
                print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()
        
        choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

        if choice == 'y':

                for file_num in range(1,10):

                        maze_name = 'maze0' + str(file_num)

                        img_file_path = img_dir_path + maze_name + '.jpg'

                        # read start and end coordinates from json file
                        start_coord, end_coord = read_start_end_coordinates("start_end_coordinates.json", maze_name)

                        print('\n============================================')
                        print('\nFor maze0' + str(file_num) + '.jpg')
        
                        # read the 'maze00.jpg' image file
                        input_img = cv2.imread(img_file_path)

                        # get the resultant warped maze image after applying Perspective Transform
                        warped_img = maze_processsor.applyPerspectiveTransform(input_img)

                        if type(warped_img) is np.ndarray:

                                # get the encoded maze in the form of a 2D array
                                maze_array = maze_processsor.detectMaze(warped_img)

                                if (type(maze_array) is list) and (len(maze_array) == 10):

                                        print('\nEncoded Maze Array = %s' % (maze_array))
                                        print('\n============================================')

                                        path = find_path(maze_array, start_coord, end_coord)

                                        if (type(path) is list):
                                                
                                                print('\nPath calculated between %s and %s is %s' % (start_coord, end_coord, path))
                                                print('\n============================================')
                                                display_path(warped_img, path, maze_name)

                                        else:
                                                print('\n Path does not exist between %s and %s' %(start_coord, end_coord))

                                else:
                                        print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                                        exit()

                        else:                           
                                print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                                exit()
        
        else:
                print()

