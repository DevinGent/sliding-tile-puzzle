# In this file a user can play a sliding tile puzzle of various sizes.

import pygame


def main():
    """Asks a user for the size of the grid they want to play on, then begins a 16-style (sliding tile) puzzle"""
    # PROMPT USER
    # puzzle_size= USER INPUT
    puzzle_size =16  #delete this later.
    play_game(puzzle_size)


def play_game(puzzle_size):
    """Sets up a grid and allows the player to play an individual puzzle."""
    pass

def move_to_empty(grid, tile):
    pass

def generate_grid(rows: int,columns: int):
    """Generates a grid of empty spaces."""
    grid=[]
    for row_number in range(rows):
        grid.append([Space(row_number*columns+i+1,row_number*columns+i+1) for i in range(columns)])
    
    for i in range(columns):
        grid[0][i].top=True
        grid[columns-1][i].bottom=True
        grid[i][0].left=True
        grid[i][columns-1].right=True

    grid[rows-1][columns-1].current_tile=0
    grid[rows-1][columns-1].correct_tile=0
    return grid

def determine_available_moves(grid: list, blank_location: set):
    """Given the coordinates of the blank tile (tile 0), this function generates a list containing the available moves as tile numbers."""
    available_moves=[]
    x=blank_location[0] 
    y=blank_location[1]
    number=None
    if grid[x][y].left==False:
        number=grid[x][y-1].current_tile
        available_moves.append(number)
    if grid[x][y].right==False:
        number=grid[x][y+1].current_tile
        available_moves.append(number)
    if grid[x][y].top==False:
        number=grid[x-1][y].current_tile
        available_moves.append(number)
    if grid[x][y].bottom==False:
        number=grid[x+1][y].current_tile
        available_moves.append(number)
    return available_moves

def move_tile(grid: list, tile_list: list, tile_number: int, display=False, surface=None):
    """Takes a grid of spaces, a list of tiles, the number of the tile to be moved, and a surface to draw on.
    The function will exchange the given tile with the blank tile and update the attributes of the Spaces and Tiles.
    If the optional argument display is set to True, then the function also animates the movement of the tile on the surface."""
    moving_tile=tile_list[tile_number]
    blank_tile=tile_list[0]
    target_vector=blank_tile.vector.copy()
    target_coordinates=blank_tile.grid_coordinates

    blank_tile.vector=moving_tile.vector.copy()
    blank_tile.update_rect()
    blank_tile.grid_coordinates=moving_tile.grid_coordinates

    grid[blank_tile.grid_coordinates[0]][blank_tile.grid_coordinates[1]].current_tile=0
    grid[target_coordinates[0]][target_coordinates[1]].current_tile=tile_number
    moving_tile.grid_coordinates=target_coordinates

    if display==False:
        moving_tile.vector=target_vector
        moving_tile.update_rect()
    else:
        moving_tiles = pygame.sprite.Group()
        moving_tiles.add(moving_tile)
  




class Tile(pygame.sprite.Sprite):
    """ 
    A tile that will move onto grid spaces
    Returns: tile object
    Functions: draw, update_rect
    Attributes: number, size, vector, rect, font, font_size, image
    """

    def __init__(self, number: int, size: int, vector: pygame.math.Vector2):
        pygame.sprite.Sprite.__init__(self) # Inherit class properties from Sprite
        # First set the number, size, and vector location of the tile.
        self.grid_coordinates= None
        self.number= number
        self.size= size
        self.vector = vector
        # Calculate an appropriate font size to fit the size of the tile.
        self.font_size=int(size/2)
        # Determine the font which will be used.
        self.font= pygame.font.SysFont('Arial', self.font_size)
        # Create a rectangle (actually a square) with edge length self.size and with the top left corner located at self.vector
        self.rect = pygame.Rect(vector, (size,size))

        # Render the tile number as a string in the font defined above.
        text=self.font.render(str(self.number), True, 'black')

        # self.image will be what gets blitted onto the file surface. Here we use SRCALPHA to ensure that the background is transparent.
        image=pygame.surface.Surface(self.rect.size, pygame.SRCALPHA)
        
        # Draw the larger square onto the image surface.
        text_rect=pygame.draw.rect(image,'light gray',((0,0),self.rect.size), border_radius=8)

        # Create a smaller rectangle (centered inside the larger) for visual effect.  
        # The size of this smaller rectangle can be controlled by adjusting size-x
        inner_rect=pygame.Rect((0,0),(size-10,size-10))
        inner_rect.center=text_rect.center
        # Draw the smaller rectangle onto the image surface
        # The width of the rectangle can be adjusted in the keyword argument.
        pygame.draw.rect(image,'dark gray',inner_rect, width=3,border_radius=8)
        # The following line of code sets text_rect to be just large enough to fit the text without moving its center.
        text_rect=text.get_rect(center=text_rect.center)
        # We blit the text onto the image in the right position (determined by text_rect)
        image.blit(text,text_rect)
        # If the tile number is 0 we turn the entire image invisible.
        if self.number==0:
            image.set_alpha(0)

        self.image=image

    def draw(self, surface):
            """Draws the image of the tile onto the given surface."""
            surface.blit(self.image,self.rect)

    def update_rect(self):
        """Updates the tile's rectangle so that it's top left corner is located at the tile's current vector."""
        self.rect.topleft=self.vector

    def move_towards_ip(self, target: pygame.math.Vector2, speed: int):
        self.vector.move_towards_ip(target, speed)
        self.update_rect()

class Space:
    """This class holds the information for grid positions.  Namely whether the given space is on the left, right, top, or bottom
    of the grid, as well as what the current tile is, and what tile should be placed there to win the game."""
    def __init__(self, current_tile, correct_tile, left=False, right=False, top=False, bottom=False):
        self.left = left
        self.right=right
        self.top=top
        self.bottom=bottom
        self.current_tile=current_tile
        self.correct_tile=correct_tile


###############################################################################
###############################################################################
# Main code. 

# Determines the size of the tiles and the spacing between them.
tile_size=80
tile_spacing=5
screen_border=20

# The following is a dictionary that lists available moves in the form tile_number: grid_coordinates
# where grid coordinates are given as a pair (row,column) 
can_move=[]

game_rows=4
game_columns=4
max_tiles=game_rows*game_columns

# This will be a list of lists containing the spaces for tiles.
grid=generate_grid(game_rows,game_columns)



i=1
for a in grid:
    print("Row", i)
    i+=1
    for b in a:
        print((b.current_tile, b.correct_tile), 
              "Left: {}, Right: {}, Top: {}, Bottom: {}  \n".format(b.left, b.right, b.top, b.bottom))


print(grid[3][2].correct_tile)
print("STOP HERE!")
print("Stopped.")

pygame.init()
# Use tiles.add(tile) for each tile to add it to the group.
tiles =pygame.sprite.Group()
moving_tiles = pygame.sprite.Group()


surface=pygame.display.set_mode(((tile_size*game_columns)+(tile_spacing*(game_columns-1))+(2*screen_border),
                                 (tile_size*game_rows)+(tile_spacing*(game_rows-1))+(2*screen_border)))
surfrect=surface.get_rect()
rectangle_pos=pygame.Vector2(0,0)
rectangle_pos2=pygame.Vector2(900,0)
rectangle=pygame.Rect(rectangle_pos,(100,100))
tile_sprite=Tile(50,80,(pygame.Vector2(500,600)))
tiles.add(tile_sprite)


# We now create a list of tiles indexed by tile number (such that the last, blank tile is labeled 0).
# We initiate a list with the first index (index 0) temporarily filled.
tile_list=[""]
# We create a tile for index 1 and locate it on the top left of the screen.
tile_list.append(Tile(1,80,(pygame.Vector2(screen_border,screen_border))))
# For the remaining indices from 2 to max_tiles-1 we place each new tile into position by modifying the position of previous tiles.
for i in range(2,max_tiles):
    # For the first row of tiles we get the new location by moving a tile size + spacing to the right of the previous tile
    if i<=game_columns:
        tile_list.append(Tile(i,
                              80,
                              pygame.Vector2(tile_list[i-1].vector.x+(tile_size+tile_spacing),
                               tile_list[i-1].vector.y)))
    # For tiles in lower rows we can get the new coordinates by                            
    else:
        tile_list.append(Tile(i,
                              80,
                              pygame.Vector2(tile_list[i-game_columns].vector.x,
                               tile_list[i-game_columns].vector.y+(tile_size+tile_spacing))))
# Finally we manually set the blank tile to go in the last space.        
tile_list[0]=Tile(0,80,pygame.Vector2(tile_list[max_tiles-1].vector.x+tile_size+tile_spacing, tile_list[max_tiles-1].vector.y))

# We add all the tiles to the Group tiles
for item in tile_list:
    tiles.add(item)

# We add the grid coordinates to each tile.
for i in range(game_rows):
    for j in range(game_columns):
        tile_list[grid[i][j].correct_tile].grid_coordinates=(i,j)


time = pygame.time.Clock()
ticks = 0

moving=False

play=True

while play==True:
    pygame.time.delay(10) 
    

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            can_move=determine_available_moves(grid,tile_list[0].grid_coordinates)
            
            for tile_number in can_move:
                if tile_list[tile_number].rect.collidepoint(event.pos):
                    print("You clicked tile {}!".format(tile_number))
                    move_tile(grid,tile_list,tile_number)
                    can_move=determine_available_moves(grid,tile_list[0].grid_coordinates)
                    print("Can move:",can_move)

    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT]: 
        print()  
        # decrement in x co-ordinate 
        for row in grid:
            for column in row:
                print(column.current_tile)
          
    # if left arrow key is pressed 
    if keys[pygame.K_RIGHT]: 
        print("Blank:",tile_list[0].grid_coordinates)
        print("Current:",grid[tile_list[0].grid_coordinates[0]][tile_list[0].grid_coordinates[1]].current_tile)
        print("Correct:",grid[tile_list[0].grid_coordinates[0]][tile_list[0].grid_coordinates[1]].correct_tile)
        # increment in x co-ordinate 
#       rectangle.x += 10 
         
    # if left arrow key is pressed    
    if keys[pygame.K_UP]: 
          
        # decrement in y co-ordinate 
        print("Tile 12:",tile_list[12].number)
        print(tile_list[12].grid_coordinates)
        print("Current:",grid[tile_list[12].grid_coordinates[0]][tile_list[12].grid_coordinates[1]].current_tile)
        print("Correct:",grid[tile_list[12].grid_coordinates[0]][tile_list[12].grid_coordinates[1]].correct_tile)
          
    # if left arrow key is pressed    
    if keys[pygame.K_DOWN]: 
        # increment in y co-ordinate 
        rectangle.y += 10
        print(target)
    if moving:
        if rectangle_pos==rectangle_pos2:
            moving=False
            print(rectangle.x)
            print("Made it!")
        else:
            rectangle_pos.move_towards_ip(target,2)
            rectangle_pos2.move_towards_ip(target,10)
            tile_sprite.vector.move_towards_ip(target,5)
            tile_sprite.rect.topleft=tile_sprite.vector



    
    pygame.draw.rect(surface,'blue',(rectangle_pos,(100,100)))
    pygame.draw.rect(surface,'red',(rectangle_pos2,(100,100)))
#    tiles.clear(surface,pygame.surface.Surface(surface.get_size()))
    tiles.clear(surface,pygame.surface.Surface(surfrect.size))
    tiles.draw(surface)

    surface.fill('black')
    tiles.draw(surface)

    

    ticks = time.tick(30) 
    # Sets a constant frame rate.
    
    pygame.display.update() 
pygame.quit()