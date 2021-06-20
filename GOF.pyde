DIM = (600, 400) # Dimension of the screen. Change as you wish.
spacing = 20 # Width of the cell. Change as you wish.

class Cell:
    def __init__(self, col, row, width_):
        self.col = col
        self.row = row
        self.width_ = width_
        self.state = False
            
    def show(self):
        if self.state:
            stroke(255, 100)
            fill(255)
        else:
            stroke(255, 100)
            fill(0)
        square(self.col, self.row, self.width_)

class Grid:
    def __init__(self, spacing, width_, height_):
        """
             `spacing` is the size of the cells.
             `width_` is the total width of the grid. 
             `height_` is the total height of the grid.
        """
        self.spacing = spacing
        self.width_ = width_
        self.height_ = height_
        self.cols = self.width_ // self.spacing
        self.rows = self.height_ // self.spacing
        self.grid = []
            
    def create(self):
        """
            Here is the structure of the self.grid:
            [ Row 1  Row 2  Row 3
             [cell1, cell2, cell3], Column 1
             [cell4, cell5, cell6], Column 2
             [cell7, cell8, cell9]  Column 3 
            ]    
        """        
        for col in range(0, self.width_, self.spacing):
            column = []
            for row in range(0, self.height_, self.spacing):
                cell = Cell(col, row, self.spacing)
                column.append(cell)
            self.grid.append(column)
    
    def show(self):        
        for col in self.grid:
            for cell in col:
                cell.show()
                
    def erase(self):
         del self.grid[:]
   
    def get_neighbors(self, column_index, row_index):
        neighbors = [
                      self.grid[(column_index + 1) % self.cols][row_index], self.grid[(column_index - 1) % self.cols][row_index],
                      self.grid[column_index][(row_index + 1) % self.rows], self.grid[column_index][(row_index - 1) % self.rows],
                      self.grid[(column_index + 1) % self.cols][(row_index + 1) % self.rows], self.grid[(column_index + 1) % self.cols][(row_index - 1) % self.rows],
                      self.grid[(column_index - 1) % self.cols][(row_index + 1) % self.rows], self.grid[(column_index - 1) % self.cols][(row_index - 1) % self.rows],
                    ]
        
        return [cell.state for cell in neighbors]
    

# read_grid = Grid(spacing, 1920, 1080) 
# write_grid = Grid(spacing, 1920, 1080)

read_grid = Grid(spacing, *DIM) 
write_grid = Grid(spacing, *DIM)
read_grid.create()

run = False

def setup():
    # fullScreen()
    size(*DIM)
    
def draw():
    global read_grid, write_grid

    """
        Algorithm:
            1) Create grid `read_grid`
            2) Create a another grid `write_grid`. Should be blank!
            3) Based on `read_grid`, fill in for `write_grid`
            4) Replace `read_grid` by `write_grid`
        Rules:     
            If a cell is alive, and has less than 2 living neighbors, then it dies.
            If a cell is alive, and has 3 or 2 living neighbors, then it survives. 
            If a cell is alive, and has more than 3 neighbors, then it dies.
            If a cell is dead, and has 3 neighbors, then it becomes alive.
    """
    if run:
        write_grid.create()
        for read_column, write_column in zip(read_grid.grid, write_grid.grid):
            for read_cell, write_cell in zip(read_column, write_column):
                column_index = read_grid.grid.index(read_column)
                row_index = read_column.index(read_cell)
                neighbors_state = read_grid.get_neighbors(column_index,row_index)        
                if read_cell.state and (neighbors_state.count(True) == 3 or neighbors_state.count(True) == 2): 
                    write_cell.state = True
                elif read_cell.state and neighbors_state.count(True) < 2:
                    write_cell.state = False
                elif read_cell.state and neighbors_state.count(True) > 3:
                    write_cell.state = False
                elif not(read_cell.state) and neighbors_state.count(True) == 3:
                    write_cell.state = True
        read_grid.erase()
        read_grid.grid = [[cell for cell in column] for column in write_grid.grid]    
        read_grid.show()
        write_grid.erase()
    else:
        read_grid.show()
            
def mouseClicked():
    global read_grid
    j, k = (mouseX // spacing, mouseY // spacing)
    cell = read_grid.grid[j][k]
    cell.state = not cell.state
    
def keyPressed():
    global run
    if key == ENTER:
        run = not run
    # If you want to save the frames    
    elif key == "s":
        saveFrame("GOF###.png")
