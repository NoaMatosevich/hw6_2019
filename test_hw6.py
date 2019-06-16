import pytest

from hw6 import*


def test_size_submarine():
    submarine = Submarine('1').__reshape__()
    assert (submarine.Shape == np.array(['1', '1', '1'])).all()


def test_size_destroyer():
    destroyer = Destroyer('1').__reshape__()
    assert (destroyer.Shape == np.array(['1', '1', '1', '1'])).all()


def test_size_jet():
    jet = Jet('1').__reshape__()
    assert (jet.Shape == np.array([[0, '1', 0, 0], ['1', '1', '1', '1'], [0, '1', 0, 0]])).all()


def test_general_size():
    general = Ship('1').__reshape__()
    assert (general.Shape == np.array(['1'])).all()


def test_ship_valid_input_name_property():
    try:
        ship = Ship(3.)
    except TypeError:
        return True
    else:
        return False


def test_board_size():
    game = Game((3, 4, 4), 1, 1, 1).create_board()
    assert game.board.size == 48


def test_num_submarines():
    game = Game((3, 4, 4), 2, 1, 1).create_board()
    num_submarine = 0
    more = True
    while more:
        submarines4comp = np.ones_like(game.board)
        submarines4comp = np.select([submarines4comp == 1], ["submarine" + str(num_submarine)])
        if (game.board == submarines4comp).any():
            num_submarine += 1
            continue
        more = False
    assert num_submarine == 2


def test_num_destroyers():
    game = Game((3, 4, 4), 1, 2, 1).create_board()
    num_destroyer = 0
    more = True
    while more:
        destroyers4comp = np.ones_like(game.board)
        destroyers4comp = np.select([destroyers4comp == 1], ["destroyer" + str(num_destroyer)])
        if (game.board == destroyers4comp).any():
            num_destroyer += 1
            continue
        more = False
    assert num_destroyer == 2


def test_num_jets():
    game = Game((3, 8, 8), 1, 1, 2).create_board()
    num_jet = 0
    more = True
    while more:
        jets4comp = np.ones_like(game.board)
        jets4comp = np.select([jets4comp == 1], ["jet" + str(num_jet)])
        if (game.board == jets4comp).any():
            num_jet += 1
            continue
        more = False
    assert num_jet == 2


def test_impossible_assignment():
    try:
        game = Game((3, 4, 4), 5, 5, 3)
    except IndexError:
        return True
    else:
        return False
