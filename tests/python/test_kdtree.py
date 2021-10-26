import py4dgeo

import numpy as np
import os
import pickle
import pytest

from . import epoch1

_test_files = [
    os.path.join(os.path.split(__file__)[0], "../data/plane_horizontal_t1.xyz")
]


@pytest.mark.parametrize("filename", _test_files)
def test_kdtree(filename):
    data = np.genfromtxt(filename)
    tree = py4dgeo.KDTree(data)
    tree.build_tree(10)

    # Find all points in sufficiently large radius
    result = tree.radius_search(np.array([0, 0, 0]), 100)
    assert result.shape[0] == data.shape[0]

    # Trigger precomputations
    tree.precompute(data[:20, :], 20)

    # Compare precomputed and real results
    for i in range(20):
        result1 = tree.radius_search(data[i, :], 5)
        result2 = tree.precomputed_radius_search(i, 5)
        assert result1.shape == result2.shape


def test_kdtree_pickle(epoch1):
    with pytest.raises(RuntimeError):
        fn = os.path.join("kdtree.pickle")
        with open(fn, "wb") as f:
            pickle.dump(epoch1.kdtree, f)
