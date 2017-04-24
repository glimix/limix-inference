from __future__ import division

from numpy import zeros, dot
from numpy import ascontiguousarray

from optimix import Function
from optimix import Vector


class LinearMean(Function):
    r"""Linear mean function.

    The mathematical representation is

    .. math::

        f(\mathbf x) = \mathbf x^\intercal \boldsymbol\alpha

    where :math:`\boldsymbol\alpha` is a vector of effect sizes.
    """
    def __init__(self, size):
        Function.__init__(self, effsizes=Vector(zeros(size)))

    def value(self, x):
        r"""Linear mean function.

        Args:
            x (array_like): covariates.

        Returns:
            :math:`\mathbf x^\intercal \boldsymbol\alpha`.
        """
        return dot(x, self.variables().get('effsizes').value)

    def gradient(self, x): # pylint: disable=R0201
        r"""Gradient of the linear mean function.

        Args:
            x (array_like): covariates.

        Returns:
            :math:`\mathbf x`.
        """
        return dict(effsizes=x)

    @property
    def effsizes(self):
        r"""Effect-sizes parameter."""
        return self.variables().get('effsizes').value

    @effsizes.setter
    def effsizes(self, v):
        self.variables().get('effsizes').value = ascontiguousarray(v)