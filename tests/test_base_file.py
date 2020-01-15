import base_file
# from nose.tools import assert_almost_equal
# import os
# import yaml

def test_nonzero_outputime():
    tot_t = base_file.total_time
    assert tot_t != 0