# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 01:45:10 2019

Most of the functions are directly taken from https://github.com/sebp/scikit-survival

@author: Kamrun Naher Keya
"""

import pandas as pd
import numpy as np



def prepare_data(x,e,t,s):

    # Sort Training Data for Accurate Likelihood
    sort_idx = np.argsort(t)[::-1]
    x = x[sort_idx]
    e = e[sort_idx]
    t = t[sort_idx]
    s = s[sort_idx]
    return (x, e, t,s)

def prepare_data3(x,e,t):

    # Sort Training Data for Accurate Likelihood
    sort_idx = np.argsort(t)[::-1]
    x = x[sort_idx]
    e = e[sort_idx]
    t = t[sort_idx]
    return (x, e, t)

from sklearn.utils import check_consistent_length, check_array

# Source: scikit-survival tool

def check_y_survival(y_or_event, *args, allow_all_censored=False):
    """Check that array correctly represents an outcome for survival analysis.
    Parameters
    ----------
    y_or_event : structured array with two fields, or boolean array
        If a structured array, it must contain the binary event indicator
        as first field, and time of event or time of censoring as
        second field. Otherwise, it is assumed that a boolean array
        representing the event indicator is passed.
    *args : list of array-likes
        Any number of array-like objects representing time information.
        Elements that are `None` are passed along in the return value.
    allow_all_censored : bool, optional, default: False
        Whether to allow all events to be censored.
    Returns
    -------
    event : array, shape=[n_samples,], dtype=bool
        Binary event indicator.
    time : array, shape=[n_samples,], dtype=float
        Time of event or censoring.
    """
    if len(args) == 0:
        y = y_or_event

        if not isinstance(y, np.ndarray) or y.dtype.fields is None or len(y.dtype.fields) != 2:
            raise ValueError('y must be a structured array with the first field'
                             ' being a binary class event indicator and the second field'
                             ' the time of the event/censoring')

        event_field, time_field = y.dtype.names
        y_event = y[event_field]
        time_args = (y[time_field],)
    else:
        y_event = np.asanyarray(y_or_event)
        time_args = args

    event = check_array(y_event, ensure_2d=False)
    if not np.issubdtype(event.dtype, np.bool_):
        raise ValueError('elements of event indicator must be boolean, but found {0}'.format(event.dtype))

    if not (allow_all_censored or np.any(event)):
        raise ValueError('all samples are censored')

    return_val = [event]
    for i, yt in enumerate(time_args):
        if yt is None:
            return_val.append(yt)
            continue

        yt = check_array(yt, ensure_2d=False)
        if not np.issubdtype(yt.dtype, np.number):
            raise ValueError('time must be numeric, but found {} for argument {}'.format(yt.dtype, i + 2))

        return_val.append(yt)

    return tuple(return_val)

def check_arrays_survival(X, y, **kwargs):
    """Check that all arrays have consistent first dimensions.
    Parameters
    ----------
    X : array-like
        Data matrix containing feature vectors.
    y : structured array with two fields
        A structured array containing the binary event indicator
        as first field, and time of event or time of censoring as
        second field.
    kwargs : dict
        Additional arguments passed to :func:`sklearn.utils.check_array`.
    Returns
    -------
    X : array, shape=[n_samples, n_features]
        Feature vectors.
    event : array, shape=[n_samples,], dtype=bool
        Binary event indicator.
    time : array, shape=[n_samples,], dtype=float
        Time of event or censoring.
    """
    event, time = check_y_survival(y)
    kwargs.setdefault("dtype", np.float64)
    X = check_array(X, ensure_min_samples=2, **kwargs)
    check_consistent_length(X, event, time)
    return X, event, time

