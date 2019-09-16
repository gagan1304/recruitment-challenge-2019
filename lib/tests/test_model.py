"""
Unit tests for the `lib.model` module

These are made using the pytest harness and cen be run with `tox`
"""

import numpy
import pytest

import lib.model


def test_moving_average():
    a = numpy.linspace(0,1,10)
    ma = lib.model.moving_average(a, 3)
    assert a.shape == ma.shape
    expected_ma = numpy.array([
        numpy.nan,
        numpy.nan,
        0.11111111,
        0.22222222,
        0.33333333,
        0.44444444,
        0.55555556,
        0.66666667,
        0.77777778,
        0.88888889,
    ])
    assert abs(numpy.nansum(ma - expected_ma)) < 1.0e-10


def test_moving_standard_deviation():    
    a = numpy.linspace(0,1,10)
    ms = lib.model.moving_standard_deviation(a, 3)
    ### XXX TODO finish this test
    expected_standard_deviation = numpy.array([
            numpy.nan,
            numpy.nan,
            0.09072184232530289,
            0.09072184232530289,
            0.09072184232530289,
            0.09072184232530292,
            0.09072184232530289,
            0.09072184232530284,
            0.09072184232530289,
            0.09072184232530293
            ])
    assert abs((ms-expected_standard_deviation).all()) < 1.0e-8
    #raise Exception("need to write a valid test for this")

def test_detect_anomalies_with_basic_input():
    n = 24 # number of hourly time stamps
    time = numpy.linspace(0, 3600.0 * (n-1), n)
    a1 = numpy.array([
        1.1,
        1.5,
        1.7,
        1.2,
        1.4,
        1.6,
        1.7,
        1.2,
        1.3,
        1.4,
        1.6,
        1.7,
        1.3,
        1.5,
        1.7,
        1.2,
        1.4,
        1.7,
        1.4,
        1.7,
        1.0,
        1.3,
        1.6,
        1.3,
    ])
    a2 = numpy.array([
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
    ])
    expected_mean_shift = numpy.array([
        numpy.nan,
        numpy.nan,
        numpy.nan,
        numpy.nan,
        numpy.nan,
        numpy.nan,
        numpy.nan,
        numpy.nan,
        numpy.nan,
        -0.543914994078,
        -0.148148148148,
        0.446949206712,
        0.503219608283,
        0.178964995882,
        -0.814835345065,
        -1.15034186819,
        -1.52026435233,
        -1.2538602834,
        -0.986539703407,
        -0.770908441441,
        -0.690290931375,
        -0.5522714852,
        -0.444576008695,
        -0.131432386301,
    ])
    expected_anomolies = [54000.0, 57600.0, 61200.0]
    result = lib.model.detect_anomalies(time, a1, a2)
    assert (result['feature'] == (a1-a2)).all()
    # XXX Test below fails because the moving_standard_deviation function isn't finished yet...
    assert abs(numpy.nansum(result['mean_shift'] - expected_mean_shift)) < 1.0e-8
    # XXX Test below fails because the anomaly detection isn't finished yet...
    assert result['anomalies'] == expected_anomolies

def test_detect_anomalies_with_empty_input():
    with pytest.raises(AssertionError):
        lib.model.detect_anomalies(numpy.array([]), numpy.array([]), numpy.array([]))

def test_detect_anomalies_with_invalid_input_types():
    with pytest.raises(AssertionError):
        lib.model.detect_anomalies([], [], [])

def test_detect_anomalies_with_invalid_input_shapes():
    with pytest.raises(AssertionError):
        lib.model.detect_anomalies(numpy.array([0.0, 1.0, 2.0]), numpy.array([1.0, 2.0]), numpy.array([1.0, 2.0]))
