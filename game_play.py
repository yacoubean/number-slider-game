from PyQt5.QtCore import QPropertyAnimation


def find_opening(tile_row,tile_col,board_locations):
    row_above = tile_row - 1
    row_below = tile_row + 1
    col_left = tile_col - 1
    col_right = tile_col + 1

    opening_found = {}

    if row_above > -1:
        tile_above = board_locations[row_above][tile_col]
        if tile_above.is_empty_tile:
            # tile above is a valid game location, and it's empty
            opening_found['qpoint'] = tile_above.position
            opening_found['new_row'] = row_above
            opening_found['new_col'] = tile_col
    if row_below < 4:
        tile_below = board_locations[row_below][tile_col]
        if tile_below.is_empty_tile:
            # tile below is a valid game location, and it's empty
            opening_found['qpoint'] = tile_below.position
            opening_found['new_row'] = row_below
            opening_found['new_col'] = tile_col
    if col_left > -1:
        tile_left = board_locations[tile_row][col_left]
        if tile_left.is_empty_tile:
            # tile left is a valid game location, and it's empty
            opening_found['qpoint'] = tile_left.position
            opening_found['new_row'] = tile_row
            opening_found['new_col'] = col_left
    if col_right < 4:
        tile_right = board_locations[tile_row][col_right]
        if tile_right.is_empty_tile:
            # tile right is a valid game location, and it's empty
            opening_found['qpoint'] = tile_right.position
            opening_found['new_row'] = tile_row
            opening_found['new_col'] = col_right

    if 'qpoint' in opening_found:
        # get the placeholder QLabel from the empty tile location
        empty_tile = board_locations[opening_found['new_row']][opening_found['new_col']]
        # store the moving tile's old position
        moving_tile_position = board_locations[tile_row][tile_col].position
        # set the moving tile's position to the empty tile's position
        board_locations[tile_row][tile_col].position = empty_tile.position
        # set the empty tile's position to its new location (the moving tile's old position)
        empty_tile.position = moving_tile_position
        # now actually move the tiles in the board_locations dictionary
        board_locations[opening_found['new_row']][opening_found['new_col']] = board_locations[tile_row][tile_col]
        board_locations[tile_row][tile_col] = empty_tile

    return opening_found


def check_move(tile_num,game_tiles,board_locations):
    this_tile_loc = game_tiles[tile_num].board_location
    tile_row_col = this_tile_loc.split('-')
    this_tile_row = int(tile_row_col[0])
    this_tile_col = int(tile_row_col[1])
    open_tile = find_opening(this_tile_row,this_tile_col,board_locations)

    return open_tile


def move_tile(new_tile_location, tile_to_move, game_layout, game_tiles):
    game_tile_to_move = game_tiles[tile_to_move]
    original_tile_loc = game_tile_to_move.board_location.split('-')
    original_tile_row = int(original_tile_loc[0])
    original_tile_col = int(original_tile_loc[1])
    game_layout.removeWidget(game_tiles[tile_to_move])
    game_layout.removeWidget(game_tiles[15]) # 15 is hard coded here because the open tile will always be tile_num=15
    game_layout.addWidget(game_tiles[15], original_tile_row, original_tile_col)
    game_layout.addWidget(game_tiles[tile_to_move], new_tile_location['new_row'], new_tile_location['new_col'])

    tile_to_move_board_loc = game_tiles[tile_to_move].board_location
    game_tiles[tile_to_move].board_location = game_tiles[15].board_location
    game_tiles[15].board_location = tile_to_move_board_loc

    game_tile_to_move.anim = QPropertyAnimation(game_tile_to_move, b"pos")
    game_tile_to_move.anim.setEndValue(new_tile_location['qpoint'])
    game_tile_to_move.anim.setDuration(200)
    game_tile_to_move.anim.start()