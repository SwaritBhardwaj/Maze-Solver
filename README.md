# Maze-Solver
Involving Computer vision techniques and path planning algorithm(A-Star) to find the path through a maze.

## Dependencies

 - pip install numpy
 - pip install python-csv
 - pip install opencv-contrib-python
 - pip install pypi-json
 
## Exploring files and folders
 - test_cases : *includes maze images*
	 - csv
	 - maze encoded output generated by maze_processor.py
	 - 10 maze images 
 - start_end_coordinates.json : *contains start and stop points for each maze image* 
 - maze_processor.py : *applies image processing techniques on maze images and returns a encoded maze in form of array*
 - display_path.py : *uses a-star agorithm to find the path using encoded maze array recieved from maze_processer.py, and displays path on image.*

## Methodology
```mermaid
graph LR
A[Input Image] -- perspective<br>transform--> B[Warped<br>Image]

B -- wall<br>detection --> C[Maze Array]
C -- encoded<br>array --> D{A-Star}
G(start_end_coordinates.json) --> D
D --computed<br>path--> F((Output))
C --> E(Saved to<br>csv folder)
```
|<img caption="Input image" src="https://user-images.githubusercontent.com/69575673/204813648-ec2010ff-5ecf-4b2d-9379-f67396e42c87.jpg" alt="drawing" width="300"/>| <img caption="Input image" src="https://user-images.githubusercontent.com/69575673/204815478-0c679391-4bc9-44b9-847c-1a8bca0cedfe.JPG" alt="drawing" width="300"/> | <img caption="Input image" src="https://user-images.githubusercontent.com/69575673/204816034-0d030d94-edab-4b34-8f31-27c1a1a9613c.JPG" alt="drawing" width="300"/> |
|:--:|:--:|:--:|
| 1. Input Image| 2. Warped Image| 3. Output Image|

