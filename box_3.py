from PIL import Image
import random

# DEFINE THINGS
BOX = 8
WALL = 0
PATH = 1
PLAYER = 9
VALID_PATH = 2
INVALID_PATH = 3
ENDPOINT = 4

LEFT = 11
RIGHT = 22
UP = 33
DOWN = 44

GAME_SOLVED = 111
GAME_FAILED = 222

COLORS = {
    WALL: (0, 0, 0),
    PATH: (255, 255, 255),
    BOX: (0, 255, 0),
    PLAYER: (255, 0, 0),
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

    img.save("step_%s.png"
             % (basename))


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
    '''
    This function simply checkes whether the block corresponding to the point is PATH or not.

    **Parameters**

        point: *tuple*
            point coordinate.
        maze: *list*

    **Returns**

        result: *boolean*
            yes or no.
    '''
    if maze[point[-1]][point[0]] == PATH:
        return True
    else:
        return False


def check_player_connectivity(board_map, player_start, player_destination):
    '''
    This function perform solely a thing:
    to check, for the given board map, whether the player can move from one location to the other.

    **Parameters**

        board map: *list*
            Current board map.
        player_start: *tuple*
            starting point.
        player_destination: *tuple*
            desired point.

    **Returns**

        valid_move_list: *boolean*
            can move to the desired point or not.
    '''
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
    '''
    This function generates a list of all the valid push move for a given board status.
    That is, a board status consists of the current map and current player location.

    **Parameters**

        board status: *list*
            Current board status.
            first thing in list is map, second is player location.

    **Returns**

        valid_push_move_list: *list*
            Potential move collected.
    '''
    board_map = board_status[0]
    player_location = board_status[-1]
    valid_push_move_list = []

    box_list = retrieve_box_coordinate(board_map)
    for box in box_list:
        if check_player_connectivity(board_map, player_location, right(box)) is True:
            if retrieve_block(board_map, left(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, LEFT))
            else:
                pass
        else:
            pass
        if check_player_connectivity(board_map, player_location, left(box)) is True:
            if retrieve_block(board_map, right(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, RIGHT))
            else:
                pass
        else:
            pass
        if check_player_connectivity(board_map, player_location, down(box)) is True:
            if retrieve_block(board_map, up(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, UP))
            else:
                pass
        else:
            pass
        if check_player_connectivity(board_map, player_location, up(box)) is True:
            if retrieve_block(board_map, down(box)) == PATH:
                valid_push_move_list.append(Push_Move(box, DOWN))
            else:
                pass
        else:
            pass

    return valid_push_move_list


def retrieve_box_coordinate(board_map):
    '''
    This function retrieves all the boxes in a given board map.

    **Parameters**

        board_map: *list*
            given board map.

    **Returns**

        box_coordinate_list: *list*
            all the boxes.
    '''
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
    '''
    This function is to find out what is the value in the board map
    for a given coordinate. Is it wall, path or box.

    **Parameters**

        board_map: *list*
            Current board map.
        coordinate: *tuple*
            given coordinate.

    **Returns**

        map_value: *int*
            find out what is for the exact block.
    '''
    x = coordinate[0]
    y = coordinate[-1]
    return board_map[y][x]


def rewrite_board(board_map, writing_point, writing_value):
    '''
    This function is to update the board map by
    rewriting values in the map.

    **Parameters**

        board_map: *list*
            Current board map.
        writing_point: *tuple*
            the point we want to write at.
        writing_value: *int*
            the value we want to write in.

    **Returns**

        None
    '''
    x = writing_point[0]
    y = writing_point[-1]
    board_map[y][x] = writing_value


class Push_Move():
    '''
    This is part of the core.
    Define a unit move in the game with two things:
    one is the location of the box, which is about to be moved,
    and the moving direction.
    '''

    def __init__(self, box_location, push_direction):
        self.box = box_location
        self.direction = push_direction


def update(board_status, push_move):
    '''
    This function updates the board status after a given push move.
    Update two things: the board map and the player location after the move.

    **Parameters**

        board_status: *list*
            Current board_status.
        push_move: *Push_Move*
            unit move.

    **Returns**

        None.
    '''
    board_status.pop()

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


def retrospect(board_status, push_move):
    '''
    This function retrospects the board status before a given push move.
    Retrospect two things: the board map and the player location before the move.

    **Parameters**

        board_status: *list*
            Current board_status.
        push_move: *Push_Move*
            unit move.

    **Returns**

        None.
    '''
    board_status.pop()

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


def generate_solution(board, target_list, player_initial):
    '''
    This function is the main body, which finds the solution for a given config.

    **Parameters**

        board: *list*
            Initial board map.
        target_list: *list*
            contains all the target location for boxes.
        player_initial: *tuple*
            player initial location.

    **Returns**

        stack_move: *list*
            all the unit moves for solution collected.
    '''
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

    while len(stack_move) > 0:
        # step 0, reset the repetition_status to False:
        repetition_status = False

        # step 1, check whether every box is at target location
        if all(retrieve_block(board_status[0], target) is BOX for target in target_list) is True:
            print("GAME_SOLVED")
            return stack_move
            # return GAME_SOLVED
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

    return GAME_FAILED


def solution_image_display(board_initial_status, list_target, stack):
    '''
    This function displays the solution in a fun and clear way.

    **Parameters**

        board_initial_status: *list*
            initial board_status.
        list_target: *list*
            target list.
        stack: *list*
            the right unit moves as the solution.

    **Returns**

        None.
    '''
    board_status = board_initial_status
    board_map = board_status[0]
    player_location = board_status[-1]
    for point in list_target:
        rewrite_board(board_map, point, ENDPOINT)
    rewrite_board(board_map, player_location, PLAYER)

    basename_num = 0
    save_maze(board_map, blockSize=20, basename=str(basename_num))

    for move in stack:
        rewrite_board(board_map, player_location, PATH)
        if move.direction == LEFT:
            player_location = right(move.box)
        elif move.direction == RIGHT:
            player_location = left(move.box)
        elif move.direction == UP:
            player_location = down(move.box)
        elif move.direction == DOWN:
            player_location = up(move.box)
        rewrite_board(board_map, player_location, PLAYER)
        basename_num = basename_num + 1
        save_maze(board_map, blockSize=20, basename=str(basename_num))

        update(board_status, move)
        board_map = board_status[0]
        rewrite_board(board_map, player_location, PATH)
        player_location = board_status[-1]
        rewrite_board(board_map, player_location, PLAYER)
        basename_num = basename_num + 1
        save_maze(board_map, blockSize=20, basename=str(basename_num))


def load_unit_test(filename):
    '''
    This function deals with readin, provided the config.

    **Parameters**

        filename: *str*
            name for the config file.

    **Returns**

        multiple_result: *tuple*
            return board map, player initial location and target list
            all to the game solving function.
    '''
    raw_string_of_file = open(filename, 'r').read()
    strings_split_by_semicolon = raw_string_of_file.strip().split(";")

    raw_board_map = strings_split_by_semicolon[0]
    raw_player_initial = strings_split_by_semicolon[1]
    raw_target_list = strings_split_by_semicolon[-1]

    cooking_board_map = raw_board_map.strip("*").split("*")
    for obj in cooking_board_map:
        if obj == "\n":
            cooking_board_map.remove(obj)
    board_map = []
    for row in cooking_board_map:
        board_map.append(row.split())
    for row in board_map:
        num = 0
        for element in row:
            if element == 'WALL':
                row[num] = WALL
            elif element == 'PATH':
                row[num] = PATH
            elif element == 'BOX':
                row[num] = BOX
            else:
                print("Error with Configuration File!!!!!")
            num = num + 1

    player_initial = (int(raw_player_initial[-4]), int(raw_player_initial[-2]))

    raw_target_list = raw_target_list.strip().split("(")
    raw_target_list.pop(0)
    target_list = []
    for raw_target in raw_target_list:
        target_list.append((int(raw_target[0]), int(raw_target[2])))

    return board_map, player_initial, target_list


if __name__ == "__main__":
    game_readin = load_unit_test("unit_test_1.data")

    test_board = game_readin[0]
    test_board_backup = []
    for row in test_board:
        test_board_backup.append([element for element in row])

    player_initial = game_readin[1]
    target_list = game_readin[-1]

    solution = generate_solution(test_board, target_list, player_initial)
    if solution != GAME_FAILED:
        solution_image_display([test_board_backup, player_initial], target_list, solution)
    else:
        print("GAME_FAILED")
