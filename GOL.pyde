DIM = (800, 600) # Dimension of the screen.
cell_width = 10

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
    def __init__(self, cell_width, width_, height_):
        """
             `cell_width` is the size of the cells.
             `width_` is the total width of the grid. 
             `height_` is the total height of the grid.
        """
        self.cell_width = cell_width
        self.width_ = width_
        self.height_ = height_
        self.cols = self.width_ // self.cell_width
        self.rows = self.height_ // self.cell_width
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
        for col in range(0, self.width_, self.cell_width):
            column = []
            for row in range(0, self.height_, self.cell_width):
                cell = Cell(col, row, self.cell_width)
                column.append(cell)
            self.grid.append(column)
    
    def show(self):        
        for col in self.grid:
            for cell in col:
                cell.show()
                
    def erase(self):
         del self.grid[:]
    
    # Makes all cells in grid dead
    def kill_cells(self):
        for column in self.grid:
            for cell in column:
                cell.state = False
         
    def show_glider(self):
        self.kill_cells()
        x = self.cols // 2
        y = self.rows // 2
        try:
            self.grid[x - 1][y].state = True
            self.grid[x + 1][y].state = True
            self.grid[x][y + 1].state = True
            self.grid[x + 1][y - 1].state = True
            self.grid[x + 1][y + 1].state = True
        except IndexError: # believe it or not this was actually helpful
            raise IndexError("Glider needs to have a bigger grid")
    
    def show_straight_line(self):
        self.kill_cells()
        y = self.rows // 2
        # 10 is an arbritrary number. You could think of it as the margin between the border's edges.
        for i in range(10, self.cols - 10):
            self.grid[i][y].state = True
        
    # Code is extremely dirty because I haven't found a better way.
    def show_gosper_glider_gun(self):
        self.kill_cells()
        x = self.cols // 2
        y = self.rows // 2
        try:
            for i in range(2):
                self.grid[x - (16 + i)][y].state = True
                self.grid[x - (16 + i)][y - 1].state = True
            
            self.grid[x - 7][y].state = True
            for i in range(3):
                self.grid[x - (7 - i)][y - (i + 1)].state = True
                self.grid[x - (7 - i)][y + (i + 1)].state = True
            
            self.grid[x - 4][y - 3].state = True
            self.grid[x - 4][y + 3].state = True
            self.grid[x - 3][y].state = True
            self.grid[x - 2][y + 2].state = True
            self.grid[x - 2][y - 2].state = True
            for i in range(3):
                self.grid[x - 1][(y + 1) - i].state = True
                
            self.grid[x][y].state = True
            
            for i in range(3):
                self.grid[x + 3][y - (i + 1)].state = True
                self.grid[x + 4][y - (i + 1)].state = True
            
            self.grid[x + 5][y - 4].state = True
            self.grid[x + 5][y].state = True
    
            for i in range(2):
                self.grid[x + 7][y - (5 - i)].state = True
                self.grid[x + 7][y + i].state = True
            
            for i in range(2):
                self.grid[x + (17 + i)][y - 2].state = True
                self.grid[x + (17 + i)][y - 3].state = True
            
        except IndexError:
            raise IndexError("Gosper Glider Gun needs to have a bigger grid")
             
    def show_pulsar(self):
        self.kill_cells()
        x = self.cols // 2
        y = self.rows // 2
        try:
            for i in range(4):
                x_inverter = 1 if (i % 2 == 0) else -1
                if i == 0:
                    y_inverter = -1
                elif i % 2 == 0:
                    y_inverter = 1
                for j in range(3):
                    self.grid[x - ((j + 2) * x_inverter)][y - (1 * y_inverter)].state = True
                    self.grid[x - ((j + 2) * x_inverter)][y - (6 * y_inverter)].state = True
                for j in range(3):
                    self.grid[x - (1 * x_inverter)][y - ((j + 2) * y_inverter)].state = True
                    self.grid[x - (6 * x_inverter)][y - ((j + 2) * y_inverter)].state = True        
        except IndexError:
            raise IndexError("Pulsar needs bigger grid")
    
    def get_neighbors(self, column_index, row_index):
        neighbors = [
                      self.grid[(column_index + 1) % self.cols][row_index], self.grid[(column_index - 1) % self.cols][row_index],
                      self.grid[column_index][(row_index + 1) % self.rows], self.grid[column_index][(row_index - 1) % self.rows],
                      self.grid[(column_index + 1) % self.cols][(row_index + 1) % self.rows], self.grid[(column_index + 1) % self.cols][(row_index - 1) % self.rows],
                      self.grid[(column_index - 1) % self.cols][(row_index + 1) % self.rows], self.grid[(column_index - 1) % self.cols][(row_index - 1) % self.rows]
                    ]
        return [cell.state for cell in neighbors]
    

# reading_grid = Grid(cell_width, 1920, 1080) 
# writing_grid = Grid(cell_width, 1920, 1080)

reading_grid = Grid(cell_width, *DIM) 
writing_grid = Grid(cell_width, *DIM)
reading_grid.create()

running = False

def setup():    
    size(*DIM)
    # fullScreen()
    
def draw():
    global reading_grid, writing_grid

    """
        Algorithm:
            1) Create grid `reading_grid`
            2) Create a another grid `writing_grid`. Should be blank!
            3) Based on `reading_grid`, fill in for `writing_grid`
            4) Replace `reading_grid` by `writing_grid`
        Rules:     
            If a cell is alive, and has less than 2 living neighbors, then it dies.
            If a cell is alive, and has 3 or 2 living neighbors, then it survives. 
            If a cell is alive, and has more than 3 neighbors, then it dies.
            If a cell is dead, and has 3 neighbors, then it becomes alive.
    """

    if running:
        writing_grid.create()
        for read_column, write_column in zip(reading_grid.grid, writing_grid.grid):
            for read_cell, write_cell in zip(read_column, write_column):
                column_index = reading_grid.grid.index(read_column)
                row_index = read_column.index(read_cell)
                neighbors_state = reading_grid.get_neighbors(column_index,row_index)        
                if read_cell.state and (neighbors_state.count(True) == 3 or neighbors_state.count(True) == 2): 
                    write_cell.state = True
                elif read_cell.state and neighbors_state.count(True) < 2:
                    write_cell.state = False
                elif read_cell.state and neighbors_state.count(True) > 3:
                    write_cell.state = False
                elif not(read_cell.state) and neighbors_state.count(True) == 3:
                    write_cell.state = True
        reading_grid.grid = [[cell for cell in column] for column in writing_grid.grid]    
        reading_grid.show()
        writing_grid.erase()
    else:
        reading_grid.show()
            
def mouseClicked():
    if not running:
        j, k = (mouseX // cell_width, mouseY // cell_width)
        cell = reading_grid.grid[j][k]
        cell.state = not cell.state
    
def keyPressed():
    global running
    if key == ENTER:
        running = not running
    elif key == "s":  # If you want to save the frames
        saveFrame("GOL###.png")
    if not running:
        if key == "c":
            reading_grid.kill_cells()
        elif key == "1":
            reading_grid.show_glider()
        elif key == "2":
            reading_grid.show_straight_line()
        elif key == "3":
            reading_grid.show_gosper_glider_gun()
        elif key == "4":
            reading_grid.show_pulsar()
