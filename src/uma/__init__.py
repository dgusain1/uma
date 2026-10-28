"""uma: collect Pyomo results as pandas DataFrames, dictionaries and arrays."""

from importlib.metadata import PackageNotFoundError, version

from uma._core import (
    get_df,
    get_dict,
    get_results_array,
    get_results_df,
    get_results_dict,
    get_value,
)

try:
    __version__ = version("uma")
except PackageNotFoundError:  # running from a source tree that isn't installed
    __version__ = "unknown"

__author__ = "Digvijay Gusain"
__all__ = [
    "get_results_df",
    "get_results_dict",
    "get_results_array",
    "get_df",  # deprecated
    "get_dict",  # deprecated
    "get_value",  # deprecated
    "__version__",
]
