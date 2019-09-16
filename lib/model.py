"""
Functions for processing and comparing the two sources of solar radiance data
"""

"""
Runs a basic algorithm to detect anomalies between two signals

Inputs:
 - time: A `numpy.ndarray` of unix times
 - signal1: A `numpy.ndarray` of the first signal
 - signal2: A `numpy.ndarray` of the second signal

Outputs:
 - A dictionary with the following keys:
    `feature`: A `numpy.ndarray` of the error between the signals
    `mean_shift`: A `numpy.ndarray` reflecting a rolling statistic of the feature
    `anomalies`: A `list` of times when there is an anomoly detected

Assumptions:
 - all arrays have the same length
 - elements of both signal arrays align with the time array
 - nan's are skipped
 - missing data isn't handled specially
"""

import numpy


def moving_average(x, w):
    """
    Calculates a rolling/moving mean across an array.

    Also substitutes in `nan` values at the start to keep resulting array length
    the same as the input.
    """
    ma = numpy.convolve(x, numpy.ones(w), 'valid') / w
    return numpy.concatenate([numpy.zeros(w-1)*numpy.nan, ma])

def moving_standard_deviation(x, w):
    """
    Calculates a rolling/moving mean across an array.

    Also substitutes in `nan` values at the start to keep resulting array length
    the same as the input.
    """
    # XXX TODO - make a rolling standard deviation.
    # Should behaviour similarly to the `moving_average` function.
    msd = numpy.zeros(x.shape)
    msd.fill(numpy.nan)
    for i in range((x.shape[0]-w+1)):
        msd[i+w-1] = x[i:i+w].std(0)
    return msd

  




def detect_anomalies(time, signal1, signal2, base_window=10, test_window=3):
    # check type of inputs
    assert isinstance(time, numpy.ndarray), "`time` argument is not an numpy.ndarray"
    assert isinstance(signal1, numpy.ndarray), "`signal1` argument is not an numpy.ndarray"
    assert isinstance(signal2, numpy.ndarray), "`signal2` argument is not an numpy.ndarray"

    # check that inputs have the same shape
    assert time.shape == signal1.shape == signal2.shape, "argument arrrays do not have the same shape"

    # check that input is long enough for the base window stats
    assert len(time) > base_window, "argument arrays are not long enough"

    # calculate a simple feature from the 2 signals
    feature = signal1 - signal2

    # calculate a mean shift score from the data
    mean_shift = numpy.zeros(time.shape)
    base_mean = moving_average(feature, base_window)
    base_std = moving_standard_deviation(feature, base_window)
    test_mean = moving_average(feature, test_window)
    mean_shift = (test_mean - base_mean) / base_std

    # detect anomalies based on the mean shift score
    anomalies = []
    # XXX TODO generate a list of times where the mean_shift is greater than or less than 1.0
    anomalies = time[mean_shift>1]
    return {
        'feature': feature,
        'mean_shift': mean_shift,
        'anomalies': anomalies,
        'base_std' : base_std,
        'test_mean' : test_mean,
        'base_mean' : base_mean,
    }
