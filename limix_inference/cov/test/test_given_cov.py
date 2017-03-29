from numpy import dot
from numpy.random import RandomState

from limix_inference.cov import GivenCov
from optimix.testing import Assertion


def test_givencov_optimix():
    item0 = 0
    item1 = 1
    K = RandomState(0).randn(5, 5)
    K = dot(K, K.T)
    a = Assertion(lambda: GivenCov(K), item0, item1, 0.0, logscale=0.0)
    a.assert_layout()
    a.assert_gradient()