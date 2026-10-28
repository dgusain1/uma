import numpy as np
import pyomo.environ as pyo
import pytest

import uma


@pytest.fixture
def model():
    m = pyo.ConcreteModel()
    m.x = pyo.Var(initialize=1.5)
    m.y = pyo.Var([1, 2, 3], initialize={1: 1.0, 2: 2.0, 3: 3.0})
    m.z = pyo.Var([("a", 1), ("a", 2), ("b", 1)], initialize=7.0)
    m.unset = pyo.Var()
    m.off = pyo.Block()
    m.off.w = pyo.Var([1], initialize=9.0)
    m.off.deactivate()
    return m


def test_get_dict(model):
    d = uma.get_results_dict(model)
    assert list(d) == ["x", "y", "z", "unset"]
    assert d["x"].tolist() == [1.5]
    assert d["y"].tolist() == [1.0, 2.0, 3.0]
    assert np.isnan(d["unset"]).all()


def test_get_df_keys_rows_by_index(model):
    df = uma.get_results_df(model)
    assert df.index.tolist() == [None, 1, 2, 3, ("a", 1), ("a", 2), ("b", 1)]
    assert df.loc[None, "x"] == 1.5
    assert df["y"][2] == 2.0
    assert df["z"][("a", 2)] == 7.0
    # no entry for a key -> NaN, not a misaligned value
    assert np.isnan(df.loc[1, "x"])
    assert np.isnan(df.loc[None, "y"])
    assert df["unset"].isna().all()


def test_get_df_empty_model():
    df = uma.get_results_df(pyo.ConcreteModel())
    assert df.empty


def test_active_flag(model):
    assert "off.w" not in uma.get_results_dict(model)
    assert "off.w" not in uma.get_results_df(model).columns
    assert "off.w" in uma.get_results_dict(model, active=False)
    assert uma.get_results_df(model, active=False)["off.w"][1] == 9.0


def test_get_value(model):
    assert uma.get_results_array(model.y).tolist() == [1.0, 2.0, 3.0]
    assert uma.get_results_array(model.x).tolist() == [1.5]


def test_version():
    assert isinstance(uma.__version__, str)


@pytest.mark.parametrize(
    "old, new",
    [("get_df", "get_results_df"), ("get_dict", "get_results_dict")],
)
def test_deprecated_model_aliases(model, old, new):
    with pytest.warns(DeprecationWarning, match=new):
        old_result = getattr(uma, old)(model)
    new_result = getattr(uma, new)(model)
    assert str(old_result) == str(new_result)


def test_deprecated_get_value(model):
    with pytest.warns(DeprecationWarning, match="get_results_array"):
        assert uma.get_value(model.x).tolist() == [1.5]
