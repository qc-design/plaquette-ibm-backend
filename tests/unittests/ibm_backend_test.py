# Copyright 2023, QC Design GmbH and the plaquette-ibm contributors
# SPDX-License-Identifier: Apache-2.0
"""Unit testing the IBMBackend."""
from unittest.mock import MagicMock

import numpy as np
from plaquette_ibm_backend.backend import IBMBackend
from qiskit.providers import JobStatus


class TestIBMBackend:
    """Unit tests for the IBMBackend."""

    def test_init(self, monkeypatch):
        """Test the initialization of IBMBackend."""
        backend_name = "simulator"
        provider_mock = MagicMock()
        provider_obj = MagicMock()
        provider_mock.return_value = provider_obj
        monkeypatch.setattr("plaquette_ibm_backend.backend.IBMProvider", provider_mock)
        backend_mock = MagicMock()
        provider_obj.get_backend.return_value = backend_mock

        device = IBMBackend(backend_name)

        provider_mock.assert_called_once()
        provider_obj.get_backend.assert_called_with(backend_name)
        assert device._backend == backend_mock
        assert device._jobs == []

    def test_run(self, monkeypatch):
        """Test the run method of IBMBackend."""
        circuit_mock = MagicMock()
        backend_mock = MagicMock()
        execute_mock = MagicMock()

        openqasm_mock = MagicMock()
        quantum_circuit_mock = MagicMock()

        monkeypatch.setattr("plaquette_ibm_backend.backend.IBMProvider", MagicMock())

        openqasm_mock.convert_to_openqasm = lambda a, ignore_unsupported: a
        quantum_circuit_mock.from_qasm_str = lambda a: a
        monkeypatch.setattr("plaquette_ibm_backend.backend.openqasm", openqasm_mock)
        monkeypatch.setattr(
            "plaquette_ibm_backend.backend.QuantumCircuit", quantum_circuit_mock
        )
        monkeypatch.setattr("plaquette_ibm_backend.backend.execute", execute_mock)

        device = IBMBackend("simulator")
        device._backend = backend_mock

        device.run(circuit_mock)

        execute_mock.assert_called_with(circuit_mock, backend=backend_mock, shots=1)
        assert len(device._jobs) == 1

    def test_get_sample(self, monkeypatch):
        """Test the get_sample method of IBMBackend."""
        monkeypatch.setattr("plaquette_ibm_backend.backend.IBMProvider", MagicMock())

        device = IBMBackend("simulator")

        # Mock the required dependencies
        job_mock1 = MagicMock()
        job_mock2 = MagicMock()
        job_mock1.result.return_value.get_counts.return_value = {"0101": 5, "1100": 3}
        job_mock2.result.return_value.get_counts.return_value = {"0011": 7}
        device._jobs = [job_mock1, job_mock2]

        # Define the expected results and erasure
        expected_results = [
            [
                np.array([1, 0, 1, 0], dtype=np.uint8),
                np.array([0, 0, 1, 1], dtype=np.uint8),
            ],
            [np.array([1, 1, 0, 0], dtype=np.uint8)],
        ]
        expected_erasure = [None, None]

        # Call the get_sample method
        results, erasure = device.get_sample()

        # Assert the results and erasure
        for r, exp_r in zip(results, expected_results):
            assert np.allclose(r, exp_r)

        assert erasure == expected_erasure
        job_mock1.result.assert_called_once()
        job_mock2.result.assert_called_once()

    def test_is_completed(self, monkeypatch):
        """Test the is_completed property of IBMBackend."""
        monkeypatch.setattr("plaquette_ibm_backend.backend.IBMProvider", MagicMock())

        device = IBMBackend("simulator")
        job_mock1 = MagicMock()
        job_mock2 = MagicMock()
        job_mock1.status.return_value = JobStatus.DONE
        job_mock2.status.return_value = JobStatus.RUNNING
        device._jobs = [job_mock1, job_mock2]

        is_completed = device.is_completed

        assert is_completed == [True, False]
        job_mock1.status.assert_called_once()
        job_mock2.status.assert_called_once()

    def test_convert_counts_to_arrays(self):
        """Verify that dictionary keys are converted to NumPy arrays."""
        input_counts = {"0101": 5, "1100": 3, "0011": 7}

        expected_output = [
            np.array([1, 0, 1, 0], dtype=np.uint8),
            np.array([0, 0, 1, 1], dtype=np.uint8),
            np.array([1, 1, 0, 0], dtype=np.uint8),
        ]

        output = IBMBackend.convert_counts_to_arrays(input_counts)

        assert np.allclose(output, expected_output)
