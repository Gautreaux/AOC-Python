from typing import List


import itertools


def neighborGeneratorFactoryND(
    min_limits: List[int], max_limits: List[int], allow_diagonal: bool
):
    assert len(min_limits) == len(max_limits)

    n_dims = len(min_limits)
    assert n_dims > 0

    def to_return(*args):
        assert len(args) == n_dims

        for offsets in itertools.product((-1, 0, 1), repeat=n_dims):
            s = sum(1 for o in offsets if o != 0)

            if s == 0:
                # no changes
                continue
            if s > 1 and allow_diagonal is False:
                # this is a diagonal change
                #   not allowed
                continue

            new_pos = tuple(map(sum, zip(args, offsets)))
            b = all(
                map(
                    lambda x, l_b, u_b: x >= l_b and x <= u_b,
                    new_pos,
                    min_limits,
                    max_limits,
                )
            )

            if b:
                yield new_pos

    return to_return


def neighborGeneratorFactory(
    max_x, max_y, min_x=0, min_y=0, allow_diagonal: bool = False
):
    """Returns a factory function that, when called with the x and y value, will generate grid neighbors
    note max_x and max_y are inclusive limits

    ex: call this function with the dimensions of your grid to get the factory object
        then for each x,y cell in the grid call the factory object to get a generator of neighbors
        the generator yields (x,y) tuples that are bounded to within the grid
            will not yield the own square back
    """
    return neighborGeneratorFactoryND((min_x, min_y), (max_x, max_y), allow_diagonal)
