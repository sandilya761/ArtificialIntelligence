
def cartesian_product(x,y):
    '''
    This function will take two iterables and returns 
    the cartesian product of them as a list
    '''
    return [a+b for a in x for b in y]


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    print('')
    
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cartesian_product(rows, cols)
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                    for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(grid_dict):
    for k,v in grid_dict.items():
        if len(v) != 1: # if the box needs elimination
            peers = peer_dict[k]    # get all the peers
            peer_values = set([grid_dict[p] for p in peers if len(grid_dict[p]) == 1])
            grid_dict[k] = ''.join(set(grid_dict[k]) - peer_values)
    return grid_dict


def only_choice(grid_dict):
    for unit in unit_list:
        for num in '123456789':
            num_places = [box for box in unit if num in grid_dict[box]]
            if len(num_places) == 1:
                grid_dict[num_places[0]] = num
    return grid_dict



def run_episode(grid_dict):
    stuck = False
    while not stuck:
        # Check how many boxes have a fixed value
        solved_values_before = len([box for box in grid_dict.keys() if len(grid_dict[box]) == 1])
        
        # Use the Eliminate Strategy
        grid_dict = eliminate(grid_dict)
        
        # Use the Only Choice Strategy
        grid_dict = only_choice(grid_dict)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in grid_dict.keys() if len(grid_dict[box]) == 1])
        
        # If no new values were added, stop the loop.
        stuck = solved_values_before == solved_values_after
        
        
        # if the current sudoku configuration is un-solvable then return False
        if len([box for box in grid_dict.keys() if len(grid_dict[box]) == 0]):
            return False 
    return grid_dict



def search(grid_dict):
    grid_dict = run_episode(grid_dict)
    
    if grid_dict is False:
        return False
    
    if all(len(v) == 1 for k,v in grid_dict.items()): 
        return grid_dict
    
    # Choose one of the unfilled squares with the fewest possibilities
    length,k = min((len(val), key) for key,val in grid_dict.items() if len(val) > 1)
    # print(k, length)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for digit in grid_dict[k]:
        new_sudoku = dict(list(grid_dict.items()))
        new_sudoku[k] = digit
        attempt = search(new_sudoku)
        if attempt:
            return attempt



if __name__ == '__main__':
    
    # this is the worlds' hardest sudoku puzzle
    start = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
    # start = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cartesian_product(rows, cols)

    row_units = [cartesian_product(r, cols) for r in rows]
    col_units = [cartesian_product(rows, c) for c in cols]
    box_units = [cartesian_product(r,c) 
                    for r in ['ABC', 'DEF', 'GHI'] 
                    for c in ['123','456','789']]

    unit_list = row_units + col_units + box_units

    # each box(key) with its units(value)
    unit_dict = dict((box, [unit for unit in unit_list if box in unit]) for box in boxes)
    
    # each box with its peers
    peer_dict = dict((box, set(sum(unit_dict[box], [])) - set([box])) for box in boxes)

    # start string converted to dictionary
    assert len(start) == 81
    grid_dict = dict(zip(boxes, start))

    # replacing the dots(.) with '123456789' (possible values in the box)
    for k,v in grid_dict.items():
        if v == '.':
            grid_dict[k] = '123456789'
            
    display(grid_dict)
    solved_grid = search(grid_dict)

    # display(grid_dict)
    display(solved_grid)

