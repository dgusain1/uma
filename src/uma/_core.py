"""Helpers to extract variable values from a solved Pyomo model."""

from __future__ import annotations

import warnings
from typing import Any, Optional

import numpy as np
import pandas as pd
import pyomo.environ as pyo


def _variables(model: pyo.Block, active: Optional[bool]):
    return model.component_objects(pyo.Var, active=active or None)


def _values(var: pyo.Var) -> dict[Any, float]:
    """Map each index of ``var`` to its value, using NaN for unset values."""
    return {
        index: np.nan if var[index].value is None else var[index].value
        for index in var
    }


def get_results_dict(model: pyo.Block, active: bool = True) -> dict[str, np.ndarray]:
    """Return the values of the variables of ``model`` as a dictionary.

    Keys are variable names; values are float arrays in index order.
    Variables without a value (e.g. unsolved) are returned as NaN.

    Args:
        model: A Pyomo model or block.
        active: If True (default), only include variables on active blocks.
            If False, include variables on deactivated blocks too.

    Example:
        >>> results = uma.get_results_dict(model)
    """
    return {
        var.name: np.fromiter(_values(var).values(), dtype=float)
        for var in _variables(model, active)
    }


def get_results_df(model: pyo.Block, active: bool = True) -> pd.DataFrame:
    """Return the values of the variables of ``model`` as a DataFrame.

    There is one column per variable and one row per Pyomo index. Rows are
    keyed by the index itself (tuples stay tuples; scalar variables use
    ``None``), so variables defined over different index sets are aligned
    on their keys, with NaN where a variable has no entry for a key.
    Row order follows first appearance across variables.

    Args:
        model: A Pyomo model or block.
        active: If True (default), only include variables on active blocks.
            If False, include variables on deactivated blocks too.

    Example:
        >>> df = uma.get_results_df(model)
        >>> df.loc[2, "y"]  # indexed variable
        >>> df["z"][("a", 2)]  # tuple keys: select the column first, since
        ...                    # df.loc[("a", 2), "z"] is read as (row, column)
    """
    columns = {var.name: _values(var) for var in _variables(model, active)}
    keys = list(dict.fromkeys(key for values in columns.values() for key in values))
    index = pd.Index(keys, dtype=object, tupleize_cols=False)
    data = {
        name: [values.get(key, np.nan) for key in keys]
        for name, values in columns.items()
    }
    return pd.DataFrame(data, index=index, dtype=float)


def get_results_array(var: pyo.Var) -> np.ndarray:
    """Return the values of a single Pyomo variable as a NumPy array.

    Example:
        >>> x = uma.get_results_array(model.x)
    """
    return np.asarray(list(var.extract_values().values()))


def _deprecated(old: str, new):
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"uma.{old} is deprecated, use uma.{new.__name__} instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return new(*args, **kwargs)

    wrapper.__name__ = old
    wrapper.__doc__ = f"Deprecated alias of :func:`{new.__name__}`."
    return wrapper


get_df = _deprecated("get_df", get_results_df)
get_dict = _deprecated("get_dict", get_results_dict)
get_value = _deprecated("get_value", get_results_array)
