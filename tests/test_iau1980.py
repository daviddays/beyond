#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from pytest import fixture, yield_fixture
from unittest.mock import patch
from numpy.testing import assert_almost_equal

from space.utils.date import Date
from space.frames.poleandtimes import ScalesDiff
from space.frames.iau1980 import _pole_motion, _precesion, _nutation, _sideral, rate


@fixture
def date():
    return Date(2004, 4, 6, 7, 51, 28, 386009)


@yield_fixture
def time():
    with patch('space.frames.poleandtimes.TimeScales.get') as mock_ts:
        mock_ts.return_value = ScalesDiff(-32.4399519, -0.4399619, 32)
        yield


@yield_fixture()
def pole_position(time):
    with patch('space.frames.poleandtimes.PolePosition.get') as mock_pole:
        mock_pole.return_value = {
            'X': -0.140682,
            'Y': 0.333309,
            'dpsi': -52.195,
            'deps': -3.875,
            'LOD': 1.5563,
        }
        yield


def test_pole_motion(date, pole_position):
    x, y = _pole_motion(date)
    assert x == -3.9078333333333335e-05
    assert y == 9.258583333333334e-05


def test_precesion(date, time):
    zeta, theta, z = _precesion(date)

    assert_almost_equal(zeta, 0.0273055)
    assert_almost_equal(theta, 0.0237306)
    assert_almost_equal(z, 0.0273059)


def test_nutation(date, pole_position):
    epsilon_bar, delta_psi, delta_eps = _nutation(date, eop_correction=False)

    assert_almost_equal(epsilon_bar, 23.4387368)
    assert_almost_equal(delta_psi, -0.0034108)
    assert_almost_equal(delta_eps, 0.0020316)


def test_sideral(date, pole_position):
    gmst = _sideral(date)
    assert_almost_equal(gmst, 312.8098943)

    gast = _sideral(date, model='apparent', eop_correction=False)
    assert_almost_equal(gast, 312.8067654)


def test_rate(date, pole_position):
    assert_almost_equal(rate(date), np.array([0, 0, 7.2921150153560662e-05]))