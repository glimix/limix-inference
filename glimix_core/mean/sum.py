from numpy import add

from optimix import Func


class SumMean(Func):
    """
    Sum mean function.

    The mathematical representation is

        F₀ + F₁ + …

    In other words, it is a sum of mean vectors.

    Parameters
    ----------
    means : list
        List of mean functions.

    Example
    -------

    .. doctest::

        >>> from glimix_core.mean import OffsetMean, LinearMean, SumMean
        >>>
        >>> X = [[5.1, 1.0],
        ...      [2.1, -0.2]]
        >>>
        >>> mean0 = LinearMean(2)
        >>> mean0.X = X
        >>> mean0.effsizes = [-1.0, 0.5]
        >>>
        >>> mean1 = OffsetMean(2)
        >>> mean1.offset = 2.0
        >>>
        >>> mean = SumMean([mean0, mean1])
        >>>
        >>> print(mean.value())
        [-2.6 -0.2]
        >>> g = mean.gradient()
        >>> print(g["SumMean[0].effsizes"])
        [[ 5.1  1. ]
         [ 2.1 -0.2]]
        >>> print(g["SumMean[1].offset"])
        [1. 1.]
        >>> mean0.name = "A"
        >>> mean1.name = "B"
        >>> mean.name = "A+B"
        >>> print(mean)
        SumMean(means=...): A+B
          LinearMean(m=2): A
            effsizes: [-1.   0.5]
          OffsetMean(): B
            offset: 2.0
    """

    def __init__(self, means):
        self._means = [c for c in means]
        Func.__init__(self, "SumMean", composite=self._means)

    def value(self):
        """
        Sum mean function., F₀ + F₁ + ….

        Returns
        -------
        M : ndarray
            F₀ + F₁ + ….
        """
        return add.reduce([mean.value() for mean in self._means])

    def gradient(self):
        """
        Sum of mean function derivatives.

        Returns
        -------
        dict
            ∂F₀ + ∂F₁ + ….
        """
        grad = {}
        for i, f in enumerate(self._means):
            for varname, g in f.gradient().items():
                grad[f"{self._name}[{i}].{varname}"] = g
        return grad

    def __str__(self):
        tname = type(self).__name__
        msg = "{}(means=...)".format(tname)
        if self.name is not None:
            msg += ": {}".format(self.name)
        for m in self._means:
            spl = str(m).split("\n")
            msg = msg + "\n" + "\n".join(["  " + s for s in spl])
        return msg
