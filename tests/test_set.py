import pytest
import raccoon as rc
from blist import blist


def test_set_cell():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'],
                          sorted=False)

    # change existing value
    actual.set(11, 'b', 55)
    assert actual.get(11, 'b') == 55
    actual.set(10, 'a', 11)
    assert actual.get(10, 'a') == 11
    actual.set(10, 'c', 13)
    assert actual.get(10, 'c') == 13
    assert actual.data == [[11, 2, 3], [4, 55, 6], [13, 8, 9]]

    # add a new row
    actual.set(13, 'b', 14)
    assert actual.data == [[11, 2, 3, None], [4, 55, 6, 14], [13, 8, 9, None]]

    # add a new column
    actual.set(13, 'd', 88)
    assert actual.data == [[11, 2, 3, None], [4, 55, 6, 14], [13, 8, 9, None], [None, None, None, 88]]

    # add a new row and column
    actual.set(14, 'e', 999)
    assert actual.data == [[11, 2, 3, None, None], [4, 55, 6, 14, None], [13, 8, 9, None, None],
                           [None, None, None, 88, None], [None, None, None, None, 999]]

    # add a new row note that index does not sort
    actual.set(1, 'a', -100)
    assert actual.data == [[11, 2, 3, None, None, -100], [4, 55, 6, 14, None, None], [13, 8, 9, None, None, None],
                           [None, None, None, 88, None, None], [None, None, None, None, 999, None]]
    assert actual.index == [10, 11, 12, 13, 14, 1]

    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])


def test_set_cell_sorted():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 12, 13], columns=['a', 'b', 'c'],
                          sorted=True)

    # change existing value
    actual.set(12, 'b', 55)
    assert actual.get(12, 'b') == 55
    actual.set(10, 'a', 11)
    assert actual.get(10, 'a') == 11
    actual.set(10, 'c', 13)
    assert actual.get(10, 'c') == 13
    assert actual.data == [[11, 2, 3], [4, 55, 6], [13, 8, 9]]

    # add a new row
    actual.set(14, 'b', 14)
    assert actual.index == [10, 12, 13, 14]
    assert actual.data == [[11, 2, 3, None], [4, 55, 6, 14], [13, 8, 9, None]]

    actual.set(11, 'a', -1)
    assert actual.index == [10, 11, 12, 13, 14]
    assert actual.data == [[11, -1, 2, 3, None], [4, None, 55, 6, 14], [13, None, 8, 9, None]]

    # add a new column
    actual.set(13, 'd', 88)
    assert actual.data == [[11, -1, 2, 3, None], [4, None, 55, 6, 14], [13, None, 8, 9, None],
                           [None, None, None, 88, None]]

    # add a new row and column
    actual.set(15, 'e', 999)
    assert actual.index == [10, 11, 12, 13, 14, 15]
    assert actual.data == [[11, -1, 2, 3, None, None], [4, None, 55, 6, 14, None], [13, None, 8, 9, None, None],
                           [None, None, None, 88, None, None], [None, None, None, None, None, 999]]
    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])

    # fails for mixed index type
    with pytest.raises(TypeError):
        actual.set('Z', 'e', 60)


def test_set_row():
    actual = rc.DataFrame({'a': [1, 3], 'b': [4, 6], 'c': [7, 9]}, index=[10, 12], columns=['a', 'b', 'c'],
                          sorted=True)

    # change existing row
    actual.set(indexes=10, values={'a': 11, 'b': 44, 'c': 77})
    assert actual.data == [[11, 3], [44, 6], [77, 9]]

    actual.set(indexes=12, values={'a': 33, 'b': 66, 'c': 99})
    assert actual.data == [[11, 33], [44, 66], [77, 99]]

    # insert new row in the middle
    actual.set(indexes=11, values={'a': 22, 'b': 5, 'c': 88})
    assert actual.data == [[11, 22, 33], [44, 5, 66], [77, 88, 99]]

    # add a new row to end
    actual.set(indexes=13, values={'a': 4, 'b': 7, 'c': 10})
    assert actual.data == [[11, 22, 33, 4], [44, 5, 66, 7], [77, 88, 99, 10]]

    actual.set(indexes=14, values={'b': 8, 'c': 11})
    assert actual.data == [[11, 22, 33, 4, None], [44, 5, 66, 7, 8], [77, 88, 99, 10, 11]]
    assert actual.index == [10, 11, 12, 13, 14]

    # add a new row to beginning
    actual.set(indexes=9, values={'a': -1, 'b': -2, 'c': -3})
    assert actual.data == [[-1, 11, 22, 33, 4, None], [-2, 44, 5, 66, 7, 8], [-3, 77, 88, 99, 10, 11]]
    assert actual.index == [9, 10, 11, 12, 13, 14]

    actual.set(indexes=8, values={'b': -3, 'c': -4})
    assert actual.data == [[None, -1, 11, 22, 33, 4, None], [-3, -2, 44, 5, 66, 7, 8], [-4, -3, 77, 88, 99, 10, 11]]
    assert actual.index == [8, 9, 10, 11, 12, 13, 14]


    # bad column names
    with pytest.raises(ValueError):
        actual.set(indexes=14, values={'a': 0, 'bad': 1})

    # bad values type
    with pytest.raises(TypeError):
        actual.set(indexes=14, values=[1, 2, 3, 4, 5])


def test_set_sorted():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'],
                          sorted=False)

    # change existing row
    actual.set(indexes=10, values={'a': 11, 'b': 44, 'c': 77})
    assert actual.data == [[11, 2, 3], [44, 5, 6], [77, 8, 9]]

    actual.set(indexes=12, values={'a': 33, 'b': 66, 'c': 99})
    assert actual.data == [[11, 2, 33], [44, 5, 66], [77, 8, 99]]

    # change subset of existing row
    actual.set(indexes=11, values={'a': 22, 'c': 88})
    assert actual.data == [[11, 22, 33], [44, 5, 66], [77, 88, 99]]

    # add a new row
    actual.set(indexes=13, values={'a': 4, 'b': 7, 'c': 10})
    assert actual.data == [[11, 22, 33, 4], [44, 5, 66, 7], [77, 88, 99, 10]]

    actual.set(indexes=14, values={'b': 8, 'c': 11})
    assert actual.data == [[11, 22, 33, 4, None], [44, 5, 66, 7, 8], [77, 88, 99, 10, 11]]
    assert actual.index == [10, 11, 12, 13, 14]

    # bad column names
    with pytest.raises(ValueError):
        actual.set(indexes=14, values={'a': 0, 'bad': 1})

    # bad values type
    with pytest.raises(TypeError):
        actual.set(indexes=14, values=[1, 2, 3, 4, 5])


def test_set_column():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'],
                          sorted=False)

    # change existing column
    actual.set(columns='b', values=[44, 55, 66])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9]]

    # add a new column
    actual.set(columns='e', values=[10, 11, 12])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9], [10, 11, 12]]
    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])

    # not enough values
    with pytest.raises(ValueError):
        actual.set(columns='e', values=[1, 2])

    # too many values
    with pytest.raises(ValueError):
        actual.set(columns='e', values=[1, 2, 3, 4])


def test_set_column_index_subset():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'],
                          sorted=False)

    # by index value
    actual.set(columns='b', indexes=[12, 11, 10], values=[66, 55, 44])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9]]

    actual.set(columns='a', indexes=[12, 10], values=[33, 11])
    assert actual.data == [[11, 2, 33], [44, 55, 66], [7, 8, 9]]

    # new rows
    actual.set(columns='c', indexes=[12, 13, 14], values=[120, 130, 140])
    assert actual.data == [[11, 2, 33, None, None], [44, 55, 66, None, None], [7, 8, 120, 130, 140]]
    assert actual.index == [10, 11, 12, 13, 14]

    # new row new columns
    actual.set(columns='z', indexes=[14, 15, 16], values=['zoo', 'boo', 'hoo'])
    assert actual.data == [[11, 2, 33, None, None, None, None], [44, 55, 66, None, None, None, None],
                           [7, 8, 120, 130, 140, None, None], [None, None, None, None, 'zoo', 'boo', 'hoo']]
    assert actual.index == [10, 11, 12, 13, 14, 15, 16]
    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])

    # values list shorter than indexes, raise error
    with pytest.raises(ValueError):
        actual.set(indexes=[10, 11], columns='a', values=[1])

    # by boolean list
    actual = rc.DataFrame({'c': [1, 2], 'a': [4, 5], 'b': [7, 8]}, index=['first', 'second'], columns=['a', 'b', 'c'],
                          sorted=False)
    actual.set(columns='c', indexes=[False, True], values=[99])
    assert actual.data == [[4, 5], [7, 8], [1, 99]]

    # boolean list not size of existing index
    with pytest.raises(ValueError):
        actual.set(indexes=[True, False, True], columns='a', values=[1, 2])

    # boolean list True entries not same size as values list
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], columns='b', values=[4, 5, 6])

    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], columns='b', values=[4])


def test_set_single_value():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'],
                      sorted=False)

    # set multiple index to one value
    df.set([10, 12], 'a', 99)
    assert df.data == [[99, 2, 99], [4, 5, 6], [7, 8, 9]]

    # set entire column to one value
    df.set(columns='c', values=88)
    assert df.data == [[99, 2, 99], [4, 5, 6], [88, 88, 88]]

    # can be anything that isn't a list
    df.set(columns='e', values={1, 2, 3})
    assert df.data == [[99, 2, 99], [4, 5, 6], [88, 88, 88], [{1, 2, 3}, {1, 2, 3}, {1, 2, 3}]]


def test_set_from_blank_df():
    # single cell
    df = rc.DataFrame(sorted=False)
    df.set(indexes=1, columns='a', values=9)
    assert df.columns == ['a']
    assert df.index == [1]
    assert df.data == [[9]]

    # single column
    df = rc.DataFrame(sorted=False)
    df.set(indexes=[1, 2, 3], columns='a', values=[9, 10, 11])
    assert df.columns == ['a']
    assert df.index == [1, 2, 3]
    assert df.data == [[9, 10, 11]]


def test_set_square_brackets():
    df = rc.DataFrame(sorted=False)

    df[1, 'a'] = 2
    assert df.data == [[2]]

    # df[[0, 3], 'b'] - - set index = [0, 3], column = b
    df[[0, 3], 'b'] = 4
    assert df.data == [[2, None, None], [None, 4, 4]]

    # df[1:2, 'b'] - - set index slice 1:2, column = b
    df[1:3, 'b'] = 5
    assert df.data == [[2, None, None], [5, 5, 5]]


def test_bar():
    df = rc.DataFrame(columns=['datetime', 'open', 'high', 'low', 'close', 'volume'], sorted=True)
    for x in range(10):
        df.set(indexes=x, values={'datetime': '2001-01-01', 'open': 100.0, 'high': 101.0, 'low': 99.5,
                                  'close': 99.75, 'volume': 10000})

    assert df.index == list(range(10))
    assert df.columns == ['datetime', 'open', 'high', 'low', 'close', 'volume']
    assert df.data[0] == ['2001-01-01'] * 10