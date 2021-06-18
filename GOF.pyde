"""
Finished on 4:40 PM, 18th of June, 2021. 
Made in collboration with my uncle, Assim Addous.
"""

DIM = (800, 800) # dimensions of the screen must be equal please ;(
dim = 45 # size of grid


# Program works well only for the first generation. Why? It just freezes.'

class Cell:
    def __init__(self, x, y, wdth):
        self.x = x
        self.y = y
        self.wdth = wdth
        self.state = False
            
    def show(self):
        if self.state:
            stroke(255)
            fill(255)
        else:
            stroke(0)
            fill(0)
        square(self.x, self.y, self.wdth)

class Grid:
    def __init__(self, dim, wdth):
        """
            `dim` is the number of rows AND columns; they must be equal so creating the 
             grid would be easier.
             `wdth` is the total width of the grid. It is usually just the screen's width (or height).
        """
        self.dim = dim
        self.wdth = wdth
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
        spacing = floor(self.wdth / self.dim) # width of each cell
        for col in range(0, self.wdth, spacing):
            column = []
            for row in range(0, self.wdth, spacing):
                cell = Cell(col, row, spacing)
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
                      self.grid[(column_index + 1) % self.dim][row_index], self.grid[(column_index - 1) % self.dim][row_index],
                      self.grid[column_index][(row_index + 1) % self.dim], self.grid[column_index][(row_index - 1) % self.dim],
                      self.grid[(column_index + 1) % self.dim][(row_index + 1) % self.dim], self.grid[(column_index + 1) % self.dim][(row_index - 1) % self.dim],
                      self.grid[(column_index - 1) % self.dim][(row_index + 1) % self.dim], self.grid[(column_index - 1) % self.dim][(row_index - 1) % self.dim],
                    ]
        
        return [cell.state for cell in neighbors]
    
    # Was used for debugging purposes, no longer needed
    # def __str__(self):
    #     return str([[cell.state for cell in column] for column in self.grid])

# Doesn't matter if we used [0] or [1]
read_grid = Grid(dim, DIM[0]) 
write_grid = Grid(dim, DIM[0])
read_grid.create()

run = False

def setup():    
    size(*DIM)
    
def mouseClicked():
    global read_grid
    spacing = DIM[0] // read_grid.dim
    k, j = (mouseY // spacing, mouseX // spacing)
    cell = read_grid.grid[j][k]
    cell.state = not cell.state
    
def draw():
    global read_grid, write_grid, run
            
    # Algorithm:
    #    1) Create grid `read_grid`
    #    2) Create a another grid `write_grid`. Should be blank!
    #    3) Based on `read_grid`, fill in for `write_grid`
    #    4) Replace `read_grid` by `write_grid` 

    """
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
    
    
def keyPressed():
    global run
    if key == ENTER:
        run = not run
