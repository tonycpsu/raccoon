import raccoon as rc
from raccoon.utils import assert_frame_equal
import pytest


def test_get_cell():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 13], columns=['a', 'b', 'c'],
                          sorted=False)

    assert actual.get(10, 'a') == 1
    assert actual.get(11, 'a') == 2
    assert actual.get(13, 'c') == 9

    # test items not in index raise errors
    with pytest.raises(ValueError):
        actual.get(1, 'a')

    with pytest.raises(ValueError):
        actual.get(100, 'a')

    with pytest.raises(ValueError):
        actual.get(12, 'a')


def test_get_cell_sorted():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 13], columns=['a', 'b', 'c'],
                          sorted=True)

    assert actual.get(10, 'a') == 1
    assert actual.get(11, 'a') == 2
    assert actual.get(13, 'c') == 9

    # test items not in index raise errors
    with pytest.raises(ValueError):
        actual.get(1, 'a')

    with pytest.raises(ValueError):
        actual.get(100, 'a')

    with pytest.raises(ValueError):
        actual.get(12, 'a')


def test_get_rows():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sorted=False)

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12], index_name='start_10', sorted=False)
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get([False, True, True, False], 'c')
    assert_frame_equal(actual, expected)

    # index out of order
    expected = rc.DataFrame({'c': [None, 7]}, index=[99, 10], index_name='start_10', sorted=False)
    actual = df.get([99, 10], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([11, 12], 'c', as_list=True) == [8, 9]

    # get as a list
    assert df.get([False, True, True, False], 'c', as_list=True) == [8, 9]

    # get entire column
    assert df.get(columns='b', as_list=True) == [4, 5, 6, 7]

    # items not in index raise errors
    with pytest.raises(ValueError):
        df.get([11, 88], 'c', as_list=True)

    # not enough items in boolean list
    with pytest.raises(ValueError):
        df.get([True, True], 'c')


def test_get_rows_sorted():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sorted=True)

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12], index_name='start_10', sorted=True)
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([11, 12], 'c', as_list=True) == [8, 9]

    # test with boolean list
    actual = df.get([False, True, True, False], 'c')
    assert_frame_equal(actual, expected)

    # index out of order
    expected = rc.DataFrame({'c': [7, None]}, index=[10, 99], index_name='start_10', sorted=True)
    actual = df.get([99, 10], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([False, True, True, False], 'c', as_list=True) == [8, 9]

    # get entire column
    assert df.get(columns='b', as_list=True) == [4, 5, 6, 7]

    # items not in index raise errors
    with pytest.raises(ValueError):
        df.get([11, 88], 'c', as_list=True)

    # not enough items in boolean list
    with pytest.raises(ValueError):
        df.get([True, True], 'c')


def test_get_columns():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sorted=False)

    expected = rc.DataFrame({'a': [4], 'c': [None]}, index=[99], columns=['a', 'c'], index_name='start_10',
                            sorted=False)
    actual = df.get(99, ['a', 'c'])
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get(99, [True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'c': [8], 'b': [5]}, index=[11], columns=['c', 'b'], index_name='start_10',
                            sorted=False)
    actual = df.get(11, ['c', 'b'])
    assert_frame_equal(actual, expected)

    # as_dict
    assert df.get_columns(11, ['b', 'c'], as_dict=True) == {'start_10': 11, 'b': 5, 'c': 8}

    # test boolean list not same length as columns
    with pytest.raises(ValueError):
        df.get(99, [True, False])

    # test index out of bounds
    with pytest.raises(ValueError):
        df.get(88, ['a', 'c'])


def test_get_columns_sorted():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sorted=True)

    expected = rc.DataFrame({'a': [4], 'c': [None]}, index=[99], columns=['a', 'c'], index_name='start_10',
                            sorted=True)
    actual = df.get(99, ['a', 'c'])
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get(99, [True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'c': [8], 'b': [5]}, index=[11], columns=['c', 'b'], index_name='start_10',
                            sorted=True)
    actual = df.get(11, ['c', 'b'])
    assert_frame_equal(actual, expected)

    # test boolean list not same length as columns
    with pytest.raises(ValueError):
        df.get(99, [True, False])

    # test index out of bounds
    with pytest.raises(ValueError):
        df.get(88, ['a', 'c'])


def test_get_matrix():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, index=['x', 'y', 'z'],
                      columns=['a', 'b', 'c', 'd'], index_name='letters', sorted=False)

    expected = rc.DataFrame({'b': [4, 6], 'd': [10, 12]}, index=['x', 'z'], columns=['b', 'd'], index_name='letters',
                            sorted=False)
    actual = df.get(['x', 'z'], ['b', 'd'])
    assert_frame_equal(actual, expected)

    # test with booleans
    actual = df.get([True, False, True], [False, True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'d': [10, 12], 'c': [7, 9]}, index=['x', 'z'], columns=['d', 'c'], index_name='letters',
                            sorted=False)
    actual = df.get(['x', 'z'], ['d', 'c'])
    assert_frame_equal(actual, expected)

    # get everything
    everything = df.get()
    assert_frame_equal(everything, df)

    # boolean list does not match index length
    with pytest.raises(ValueError):
        df.get([True, False], [False, True, False, True])

    # boolean list does not match columns length
    with pytest.raises(ValueError):
        df.get([True, False, True], [False, True])

    # missing index
    with pytest.raises(ValueError):
        df.get_matrix(['BAD', 'x'], ['a', 'b'])

    # missing column
    with pytest.raises(ValueError):
        df.get_matrix(['x', 'y'], ['a', 'b', 'BAD'])


def test_get_matrix_sorted():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6], 'c': [8, 7, 9], 'd': [11, 10, 12]}, index=['y', 'x', 'z'],
                      columns=['a', 'b', 'c', 'd'], index_name='letters', sorted=True)

    expected = rc.DataFrame({'b': [4, 6], 'd': [10, 12]}, index=['x', 'z'], columns=['b', 'd'], index_name='letters',
                            sorted=True)
    actual = df.get(['x', 'z'], ['b', 'd'])
    assert_frame_equal(actual, expected)

    # test with booleans
    actual = df.get([True, False, True], [False, True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'d': [10, 12], 'c': [7, 9]}, index=['x', 'z'], columns=['d', 'c'], index_name='letters',
                            sorted=True)
    actual = df.get(['x', 'z'], ['d', 'c'])
    assert_frame_equal(actual, expected)

    # get everything
    everything = df.get()
    assert_frame_equal(everything, df)

    # boolean list does not match index length
    with pytest.raises(ValueError):
        df.get([True, False], [False, True, False, True])

    # boolean list does not match columns length
    with pytest.raises(ValueError):
        df.get([True, False, True], [False, True])

    # missing index
    with pytest.raises(ValueError):
        df.get_matrix(['BAD', 'x'], ['a', 'b'])

    # missing column
    with pytest.raises(ValueError):
        df.get_matrix(['x', 'y'], ['a', 'b', 'BAD'])


def test_get_locations():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, index=[2, 4, 6, 8])

    assert_frame_equal(df.get_locations([0, 2]), rc.DataFrame({'a': [1, 3], 'b': [5, 7]}, index=[2, 6]))
    assert_frame_equal(df.get_locations([1, 3], 'a'), rc.DataFrame({'a': [2, 4]}, index=[4, 8]))
    assert df.get_locations([0, 2], 'b', as_list=True) == [5, 7]


def test_get_square_brackets():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sorted=False)

    # df['b'] -- get column
    assert_frame_equal(df['b'], rc.DataFrame({'b': [4, 5, 6]}, sorted=False))

    # df[['a', 'b', c']] -- get columns
    assert_frame_equal(df[['a', 'b', 'c']], rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                                                         columns=['a', 'b', 'c'], sorted=False))

    assert_frame_equal(df[['c', 'a']], rc.DataFrame({'c': [7, 8, 9], 'a': [1, 2, 3]}, columns=['c', 'a'], sorted=False))

    # df[1, 'd'] -- get cell at index = 5, column = 'b'
    assert df[1, 'd'] == 11

    # df[[0, 2]] -- get indexes = [0, 2] all columns
    assert_frame_equal(df[[0, 2], df.columns],
                       rc.DataFrame({'a': [1, 3], 'b': [4, 6], 'c': [7, 9], 'd': [10, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[0, 2], sorted=False))

    assert_frame_equal(df[[2, 1], df.columns],
                       rc.DataFrame({'a': [3, 2], 'b': [6, 5], 'c': [9, 8], 'd': [12, 11]},
                                    columns=['a', 'b', 'c', 'd'], index=[2, 1], sorted=False))

    # df[[0, 2], 'c'] -- get indexes = [4, 5], column = 'b'
    assert_frame_equal(df[[0, 2], 'c'], rc.DataFrame({'c': [7, 9]}, index=[0, 2], sorted=False))

    assert_frame_equal(df[[2, 0], 'c'], rc.DataFrame({'c': [9, 7]}, index=[2, 0], sorted=False))

    # df[[1, 2], ['a', 'd']] -- get indexes = [4, 5], columns = ['a', 'b']
    assert_frame_equal(df[[1, 2], ['a', 'd']], rc.DataFrame({'a': [2, 3], 'd': [11, 12]}, columns=['a', 'd'],
                       index=[1, 2], sorted=False))

    assert_frame_equal(df[[2, 0], ['d', 'a']], rc.DataFrame({'d': [12, 10], 'a': [3, 1]}, columns=['d', 'a'],
                       index=[2, 0], sorted=False))


def test_get_square_brackets_sorted():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sorted=True)

    # df['b'] -- get column
    assert_frame_equal(df['b'], rc.DataFrame({'b': [4, 5, 6]}, sorted=True))

    # df[['a', 'b', c']] -- get columns
    assert_frame_equal(df[['a', 'b', 'c']], rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                                                         columns=['a', 'b', 'c'], sorted=True))

    assert_frame_equal(df[['c', 'a']], rc.DataFrame({'c': [7, 8, 9], 'a': [1, 2, 3]}, columns=['c', 'a'], sorted=True))

    # df[1, 'd'] -- get cell at index = 5, column = 'b'
    assert df[1, 'd'] == 11

    # df[[0, 2]] -- get indexes = [0, 2] all columns
    assert_frame_equal(df[[0, 2], df.columns],
                       rc.DataFrame({'a': [1, 3], 'b': [4, 6], 'c': [7, 9], 'd': [10, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[0, 2], sorted=True))

    assert_frame_equal(df[[2, 1], df.columns],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2], sorted=True))

    # df[[0, 2], 'c'] -- get indexes = [4, 5], column = 'b'
    assert_frame_equal(df[[0, 2], 'c'], rc.DataFrame({'c': [7, 9]}, index=[0, 2], sorted=True))

    assert_frame_equal(df[[2, 0], 'c'], rc.DataFrame({'c': [9, 7]}, index=[2, 0], sorted=True))

    # df[[1, 2], ['a', 'd']] -- get indexes = [4, 5], columns = ['a', 'b']
    assert_frame_equal(df[[1, 2], ['a', 'd']], rc.DataFrame({'a': [2, 3], 'd': [11, 12]}, columns=['a', 'd'],
                       index=[1, 2], sorted=True))

    assert_frame_equal(df[[2, 0], ['d', 'a']], rc.DataFrame({'d': [10, 12], 'a': [1, 3]}, columns=['d', 'a'],
                       index=[0, 2], sorted=True))


def test_get_slicer():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sorted=False)

    # df[1:2] -- get slice from index 1 to 2, all columns
    assert_frame_equal(df[1:2],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2], sorted=False))

    # df[0:1, ['c', 'd']] -- get slice from index 0 to 1, columns ['c', 'd']
    assert_frame_equal(df[0:1, ['c', 'd']], rc.DataFrame({'c': [7, 8], 'd': [10, 11]},
                                                         columns=['c', 'd'], index=[0, 1], sorted=False))

    assert_frame_equal(df[0:1, ['d', 'c']], rc.DataFrame({'d': [10, 11], 'c': [7, 8]},
                                                         columns=['d', 'c'], index=[0, 1], sorted=False))

    # df[1:1, 'c'] -- get slice 1 to 1 and column 'c'
    assert_frame_equal(df[1:1, 'c'], rc.DataFrame({'c': [8]}, index=[1], sorted=False))

    # test indexes not in the range
    with pytest.raises(IndexError):
        x = df[4:5, 'c']

    with pytest.raises(IndexError):
        x = df[0:8, 'c']

    with pytest.raises(IndexError):
        x = df[2:1, 'c']


def test_get_slicer_sorted():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sorted=True)

    # df[1:2] -- get slice from index 1 to 2, all columns
    assert_frame_equal(df[1:2],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2], sorted=True))

    # df[0:1, ['c', 'd']] -- get slice from index 0 to 1, columns ['c', 'd']
    assert_frame_equal(df[0:1, ['c', 'd']], rc.DataFrame({'c': [7, 8], 'd': [10, 11]},
                                                         columns=['c', 'd'], index=[0, 1], sorted=True))

    assert_frame_equal(df[0:1, ['d', 'c']], rc.DataFrame({'d': [10, 11], 'c': [7, 8]},
                                                         columns=['d', 'c'], index=[0, 1], sorted=True))

    # df[1:1, 'c'] -- get slice 1 to 1 and column 'c'
    assert_frame_equal(df[1:1, 'c'], rc.DataFrame({'c': [8]}, index=[1], sorted=True))

    # test indexes not in the range
    with pytest.raises(IndexError):
        x = df[4:5, 'c']

    with pytest.raises(IndexError):
        x = df[0:8, 'c']

    with pytest.raises(IndexError):
        x = df[2:1, 'c']


def test_head():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False)

    assert_frame_equal(df.head(0), rc.DataFrame(columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(1), rc.DataFrame({1: [0], 2: [3]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(2), rc.DataFrame({1: [0, 1], 2: [3, 4]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))


def test_tail():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False)

    assert_frame_equal(df.tail(0), rc.DataFrame(columns=[1, 2], sorted=False))
    assert_frame_equal(df.tail(1), rc.DataFrame({1: [2], 2: [5]}, columns=[1, 2], index=[2], sorted=False))
    assert_frame_equal(df.tail(2), rc.DataFrame({1: [1, 2], 2: [4, 5]}, columns=[1, 2], index=[1, 2], sorted=False))
    assert_frame_equal(df.tail(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.tail(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))
