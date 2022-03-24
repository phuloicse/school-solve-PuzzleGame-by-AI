# solve-PuzzleGame-by-AI



# Tents and Tree 
* The game rules and samples can be found here: https://www.puzzle-tents.com/
## How to run the solver 
### Step 1: Add the input to the game:
    **Example:**
    
    ![Sample board.](https://scontent.xx.fbcdn.net/v/t1.15752-9/276123273_1144364023046939_2909223102056351214_n.png?stp=dst-png_s206x206&_nc_cat=100&ccb=1-5&_nc_sid=aee45a&_nc_ohc=JsWv8tycIZcAX9Yo4lC&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVIKU3vPXizW3-LnHrEqmrIFc0NgKgXwcEDXRIABRAiCKg&oe=62601548 "Sample board")
    
    Will be preresented by the text input:
    ```
    _112012
    3#T#T##
    0####T#
    1###T##
    1######
    1##T##T
    1####T#
    ```
    ### Unordered
    * _ : unused value 
    * '#' : an empty cell
    * 'T' : a tree cell 
    * 'A' : a tent cell 
    * 'number': the tents required on this col / row 


### Step 2: Run the solver 
   ```
    cd ./Tents && python tents_solver.py input_name.txt 
   ```

#####    To save the image of the solution: 
   ```
    cd ./Tents && python tents_solver.py input_name.txt output_name.png  
   ```

##### Sample solution image

![Sample solution image.](https://scontent.xx.fbcdn.net/v/t1.15752-9/275221540_1158117001399555_2174703013123145628_n.png?stp=dst-png_s206x206&_nc_cat=107&ccb=1-5&_nc_sid=aee45a&_nc_ohc=eC914PU7ZmgAX-TQBCs&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJtIqbKIfXmT0NqVHOClOo-ogbpmKBg1bLmy_RK8YZ3vw&oe=6260C102 "Sample solution image")
    
   
