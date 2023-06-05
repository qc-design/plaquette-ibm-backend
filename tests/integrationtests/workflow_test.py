# Copyright 2023, QC Design GmbH and the plaquette-ibm contributors
# SPDX-License-Identifier: Apache-2.0
"""Integration testing the plugin."""
import os

import numpy as np
import pytest
from qiskit_ibm_provider import IBMProvider

import plaquette
from plaquette.circuit import Circuit


def ensure_account_saved():
    """Make sure that an account is stored, otherwise save one with a token."""
    if not IBMProvider.saved_accounts():
        token = os.getenv("IBM_TOKEN", None)
        IBMProvider.save_account(token)


# Open issues: https://github.com/Qiskit/qiskit-ibm-provider/issues/604
@pytest.mark.xfail(reason="Bug with new qiskit-ibm-provider")
@pytest.mark.e2e
@pytest.mark.parametrize(
    "circuit_str, expected",
    [
        ("M 0 1 2", np.array([0, 0, 0])),
        ("X 0\nM 0 1 2", np.array([1, 0, 0])),
        ("X 1\nM 0 1 2", np.array([0, 1, 0])),
        ("X 1\nX 2\nM 0 1 2", np.array([0, 1, 1])),
    ],
)
def test_integration(circuit_str, expected):
    """Test that plaquette integrates well with the IBM backend."""
    ensure_account_saved()
    circuit = Circuit.from_str(circuit_str)

    # Add the ability to select least busy
    system_name = "simulator_stabilizer"
    dev = plaquette.Device("ibm", system_name=system_name)
    dev.run(circuit)
    samples, er = dev.get_sample()
    assert np.allclose(samples, expected)
    assert er is None
