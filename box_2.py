import time
import random

# DEFINE THINGS
VOID = 9
BOX = 8
WALL = 0
PATH = 1
VALID_PATH = 2
INVALID_PATH = 3
ENDPOINT = 4

LEFT = 11
RIGHT = 22
UP = 33
DOWN = 44

GAME_SOLVED = 111

COLORS = {
    WALL: (0, 0, 0),
    PATH: (255, 255, 255),
    VALID_PATH: (0, 255, 0),
    INVALID_PATH: (255, 0, 0),
    ENDPOINT: (0, 0, 255),
}


def set_color(img, x0, y0, dim, color):
    '''
    This functions sets the color of the block in the maze.
    Every pixel in the same block shares the same color.
    The standard color representation is set above.

    **Parameters**

        img: *int*
            The image file we would like to put every set pixel in.
        x0: *int*
            X coordinate of the block in the maze.
        y0: *int*
            Y coordinate of the block in the maze.
        dim: *int*
            Correspond to the blocksize.
        color: *tuple*
            The color we would like to paint the block with 
            by visting the standard color dictionary.

    **Return**

        None
    '''
    for x in range(dim):
        for y in range(dim):
            img.putpixel(
                (dim * x0 + x, dim * y0 + y),
                color
            )


def save_maze(maze, blockSize=20, basename="maze"):
    '''
    This function saves the generated maze or maze solution to a png file.

    **Parameters**

        maze: *list*
            The maze we want to save to a file.
        blockSize: *int*
        basename: *str*
            The name we would like to name our file.

    **Returns**

        None
    '''
    w_blocks = len(maze[0])
    h_blocks = len(maze)
    SIZE = (w_blocks * blockSize, h_blocks * blockSize)
    img = Image.new("RGB", SIZE, color=COLORS[WALL])

    for y, row in enumerate(maze):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])

    img.save("%s_%d_%d_%d.png"
             % (basename, w_blocks, h_blocks, blockSize))


def load_maze(filename, ext=".png"):
    '''
    This function loads a file from the folder and convert it into a maze list
    for further processing.

    **Parameters**

        filename: *str*
        ext: *str*

    **Returns**

        mutilple_info: *list*
            This data consists of two part.
            One is the maze itself in a list type.
            The other is the blocksize.
    '''
    img = Image.open(filename)
    raw_data = filename.strip(".png").split("_")
    blockSize = int(raw_data[-1])
    height = int(raw_data[-2])
    width = int(raw_data[-3])
    x_samples = [x * blockSize for x in range(width)]
    y_samples = [y * blockSize for y in range(height)]

    maze = [
        [WALL for _ in range(width)]
        for _ in range(height)
    ]

    for x in range(width):
        for y in range(height):
            pxl = img.getpixel((x_samples[x], y_samples[y]))
            if pxl[0] == 255:
                maze[y][x] = PATH
    return [maze, blockSize]


def up(point):
    '''
    This function, as well as the three below, handles the moving of the point,
    only in different direction.

    **Parameters**

        point: *tuple*
            Current point coordinate.

    **Returns**

        new_point:*tuple*
            New point coordinate.
    '''
    return (point[0], point[1] - 1)


def down(point):
    '''
    **Parameters**

        point: *tuple*
            Current point coordinate.

    **Returns**

        new_point:*tuple*
            New point coordinate.
    '''
    return (point[0], point[1] + 1)


def left(point):
    '''
    **Parameters**

        point: *tuple*
            Current point coordinate.

    **Returns**

        new_point:*tuple*
            New point coordinate.
    '''
    return (point[0] - 1, point[1])


def right(point):
    '''
    **Parameters**

        point: *tuple*
            Current point coordinate.

    **Returns**

        new_point:*tuple*
            New point coordinate.
    '''
    return (point[0] + 1, point[1])


def generate_valid_move_list_for_solving(current_point, maze):
    '''
    This function is to create a list for further randomly choosing one step
    to go ahead, only when solving the maze.
    In this case, we need to know all eligible moves.

    **Parameters**

        current_point: *tuple*
            Current point coordinate.
        maze: *list*

    **Returns**

        valid_move_list: *list*
            Potential move collected.
    '''
    valid_move_list = []
    if valid_move_check_for_solving(up(current_point), maze) is True:
        valid_move_list.append(up(current_point))
    if valid_move_check_for_solving(down(current_point), maze) is True:
        valid_move_list.append(down(current_point))
    if valid_move_check_for_solving(left(current_point), maze) is True:
        valid_move_list.append(left(current_point))
    if valid_move_check_for_solving(right(current_point), maze) is True:
        valid_move_list.append(right(current_point))
    return valid_move_list


def valid_move_check_for_solving(point, maze):
    if maze[point[-1]][point[0]] == PATH:
        return True
    else:
        return False





def check_player_connectivity(board_map, player_start, player_destination):

    maze = []
    for row in board_map:
        maze.append([element for element in row])


    stack = [player_start]

    # blockSize = load_maze(filename)[-1]

    x, y = stack[-1]
    maze[y][x] = VALID_PATH
    if stack[-1] == player_destination:
        return True

    while len(stack) > 0:
        if generate_valid_move_list_for_solving(stack[-1], maze) != []:
            stack.append(random.choice(generate_valid_move_list_for_solving(stack[-1], maze)))
            if stack[-1] == player_destination:
                return True
            else:
                pass
            x, y = stack[-1]
            maze[y][x] = VALID_PATH
        else:
            x, y = stack[-1]
            maze[y][x] = INVALID_PATH
            stack.pop()
    
    return False

def generate_valid_push_move_list(board_status):
    board_map = board_status[0]
    player_location = board_status[-1]
    valid_push_move_list = []

    box_list = retrieve_box_coordinate(board_map)
    for box in box_list:
        if check_player_connectivity(board_map, player_location, right(box)) is True:
            if retrieve_block(board_map, left(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, LEFT))
                print("LEFT YES!!")
            else:
                pass
        else:
            pass
        if check_player_connectivity(board_map, player_location, left(box)) is True:
            if retrieve_block(board_map, right(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, RIGHT))
                print("RIGHT YES!!")
            else:
                pass
        else:
            pass
        if check_player_connectivity(board_map, player_location, down(box)) is True:
            if retrieve_block(board_map, up(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, UP))
                print("UP YES!!")
            else:
                pass
        else:
            pass
        if check_player_connectivity(board_map, player_location, up(box)) is True:
            if retrieve_block(board_map, down(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, DOWN))
                print("DOWN YES!!")
            else:
                pass
        else:
            pass

    return valid_push_move_list


def retrieve_box_coordinate(board_map):
    box_coordinate_list = []
    y = 0
    for row in board_map:
        x = 0
        for block in row:
            if block == BOX:
                box_coordinate_list.append((x, y))
            x = x + 1
        y = y + 1
    return box_coordinate_list


def retrieve_block(board_map, coordinate):
    x = coordinate[0]
    y = coordinate[-1]
    return board_map[y][x]


def rewrite_board(board_map, writing_point, writing_value):
    x = writing_point[0]
    y = writing_point[-1]
    board_map[y][x] = writing_value


class Push_Move():
    def __init__(self, box_location, push_direction):
        self.box = box_location
        self.direction = push_direction


def update(board_status, push_move):
    push_direction = push_move.direction
    board_status.pop()

    print("----------------------------------")
    print(retrieve_box_coordinate(board_status[0]))
    print("begin update")

    if push_move.direction == LEFT:
        board_status.append((push_move.box[0], push_move.box[-1]))

        rewrite_board(board_status[0], push_move.box, PATH)
        rewrite_board(board_status[0], left(push_move.box), BOX)

    elif push_move.direction == RIGHT:
        board_status.append((push_move.box[0], push_move.box[-1]))

        rewrite_board(board_status[0], push_move.box, PATH)
        rewrite_board(board_status[0], right(push_move.box), BOX)

    elif push_move.direction == UP:
        board_status.append((push_move.box[0], push_move.box[-1]))

        rewrite_board(board_status[0], push_move.box, PATH)
        rewrite_board(board_status[0], up(push_move.box), BOX)

    else:
        board_status.append((push_move.box[0], push_move.box[-1]))

        rewrite_board(board_status[0], push_move.box, PATH)
        rewrite_board(board_status[0], down(push_move.box), BOX)

    print(retrieve_box_coordinate(board_status[0]))
    print("----------------------------------")


def retrospect(board_status, push_move):
    push_direction = push_move.direction
    board_status.pop()

    print("----------------------------------")
    print(retrieve_box_coordinate(board_status[0]))
    print("begin retrospect")

    if push_move.direction == LEFT:
        board_status.append((right(push_move.box)[0], right(push_move.box)[-1]))

        rewrite_board(board_status[0], push_move.box, BOX)
        rewrite_board(board_status[0], left(push_move.box), PATH)

    elif push_move.direction == RIGHT:
        board_status.append((right(push_move.box)[0], right(push_move.box)[-1]))

        rewrite_board(board_status[0], push_move.box, BOX)
        rewrite_board(board_status[0], right(push_move.box), PATH)

    elif push_move.direction == UP:
        board_status.append((right(push_move.box)[0], right(push_move.box)[-1]))

        rewrite_board(board_status[0], push_move.box, BOX)
        rewrite_board(board_status[0], up(push_move.box), PATH)

    else:
        board_status.append((right(push_move.box)[0], right(push_move.box)[-1]))

        rewrite_board(board_status[0], push_move.box, BOX)
        rewrite_board(board_status[0], down(push_move.box), PATH)

    print(retrieve_box_coordinate(board_status[0]))
    print("----------------------------------")


def generate_solution(board, target_list, player_initial):
    target_list = target_list

    board_status = [board, player_initial]
    board_status_list = []

    temp_1 = []
    temp_2 = (board_status[-1][0], board_status[-1][-1])
    for row in board_status[0]:
        temp_1.append([element for element in row])
    board_status_list.append([temp_1, temp_2])

    valid_push_move_list = generate_valid_push_move_list(board_status)


    stack_move = []
    stack_possibility = []
    stack_possibility.append(valid_push_move_list)



    stack_move.append(stack_possibility[-1][-1])
    update(board_status, stack_move[-1])
    stack_possibility[-1].pop()


    while 1:
        # step 0, reset the repetition_status to False:
        print("*****NEW ROUND*****")
        repetition_status = False

        # step 1, check whether every box is at target location
        if all(retrieve_block(board_status[0], target) is BOX for target in target_list) is True:
            print("GAME_SOLVED")
            return GAME_SOLVED
        else:
            pass

        # step 2, check wheher the current board status has occured
        for archive_board_status in board_status_list:
            if board_status[0] == archive_board_status[0]:
                if check_player_connectivity(board_status[0], board_status[-1], archive_board_status[-1]) is True:
                    repetition_status = True
                    break
                else:
                    pass
            else:
                pass

        if repetition_status is True:
            print True
            retrospect(board_status, stack_move[-1])
            stack_move.pop()
            while stack_possibility[-1] == []:
                retrospect(board_status, stack_move[-1])
                stack_move.pop()
                stack_possibility.pop()

            stack_move.append(stack_possibility[-1][-1])
            update(board_status, stack_move[-1])
            stack_possibility[-1].pop()
            continue
        else:
            print False
            temp_1 = []
            temp_2 = (board_status[-1][0], board_status[-1][-1])
            for row in board_status[0]:
                temp_1.append([element for element in row])
            board_status_list.append([temp_1, temp_2])

        # step 3 find all the possible pushing moves (if there is any), and put in a list.
        valid_push_move_list = generate_valid_push_move_list(board_status)
        if valid_push_move_list == []:
            retrospect(board_status, stack_move[-1])
            stack_move.pop()
            while stack_possibility[-1] == []:
                retrospect(board_status, stack_move[-1])
                stack_move.pop()
                stack_possibility.pop()

            stack_move.append(stack_possibility[-1][-1])
            update(board_status, stack_move[-1])
            stack_possibility[-1].pop()
            continue
        else:
            stack_possibility.append(valid_push_move_list)
            stack_move.append(stack_possibility[-1][-1])
            update(board_status, stack_move[-1])
            stack_possibility[-1].pop()






if __name__ == "__main__":
    test_board = [
        [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
        [WALL, PATH, PATH, PATH, PATH, PATH, PATH, PATH, WALL],
        [WALL, PATH, BOX, PATH, PATH, PATH, PATH, PATH, WALL],
        [WALL, PATH, PATH, WALL, PATH, PATH, PATH, WALL, WALL],
        [WALL, WALL, WALL, WALL, WALL, WALL, PATH, WALL],
        [VOID, VOID, VOID, VOID, VOID, WALL, PATH, WALL],
        [VOID, VOID, VOID, VOID, VOID, WALL, WALL, WALL]
    ]

    # test_board = [
    #     [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    #     [WALL, PATH, PATH, PATH, PATH, PATH, PATH, PATH, WALL],
    #     [WALL, PATH, BOX, PATH, PATH, PATH, PATH, PATH, WALL],
    #     [WALL, PATH, PATH, PATH, PATH, PATH, PATH, PATH, WALL],
    #     [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]
    # ]

    player_initial = (1, 2)
    # meaning test_board[2][1] should be PLAYER
    target_list = [(7, 1)]

    generate_solution(test_board, target_list, player_initial)


    # save_maze(test_maze, blockSize=20)
    # generate_maze(50, 50)
    # solve_maze("maze_50_50_20.png")



































