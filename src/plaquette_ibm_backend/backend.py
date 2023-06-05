# Copyright 2023, QC Design GmbH and the plaquette-ibm contributors
# SPDX-License-Identifier: Apache-2.0
"""Base quantum device class."""
from typing import Any, List, Optional, Tuple, Union

import numpy as np
from qiskit import QuantumCircuit, execute
from qiskit.providers import Job, JobStatus
from qiskit_ibm_provider import IBMProvider

from plaquette import circuit as plaq_circuit
from plaquette.circuit import openqasm


class IBMBackend:
    """Quantum device for accessing IBM's simulators or real quantum systems.

    .. automethod:: __init__
    """

    def __init__(
        self,
        system_name: str,
    ):
        """Create a new quantum device using an IBM Quantum system.

        Args:
            system_name: The name of the IBM Quantum system or simulator to use.

        Notes:
            Arguments and keywords arguments are not checked on device
            creation.
        """
        provider = IBMProvider()
        self._backend = provider.get_backend(system_name)
        self._jobs: List[Job] = []

    def run(
        self,
        circuit: plaq_circuit.Circuit | plaq_circuit.CircuitBuilder,
        *,
        shots=1,
    ):
        """Run the given circuit.

        Args:
            circuit: The circuit (or the builder containing it) to be simulated.

        Keyword Args:
            shots: the number of shots to run the circuit with on IBM's system.
        """
        circ = openqasm.convert_to_openqasm(circuit, ignore_unsupported=True)
        qiskit_circuit = QuantumCircuit.from_qasm_str(circ)
        job = execute(qiskit_circuit, backend=self._backend, shots=shots)
        self._jobs.append(job)

    @staticmethod
    def convert_counts_to_arrays(input_counts) -> Union[list, np.ndarray]:
        """Convert basis states to samples format as used in plaquette.

        Args:
            input_counts: A dictionary where the keys are strings of 0s and 1s,
                and the values are counts or integers.

        Returns:
            list: A list of NumPy arrays where each element is a key from the input
                  dictionary cast to a NumPy array.

        Example:
            >>> input_counts = {
            ...     '0101': 5,
            ...     '1100': 3,
            ...     '0011': 7
            ... }
            >>> convert_counts_to_arrays(input_counts)
            [array([0, 1, 0, 1], dtype=uint8),
             array([1, 1, 0, 0], dtype=uint8),
             array([0, 0, 1, 1], dtype=uint8)]
        """
        # Note: the basis state ordering of Qiskit is reversed compared to plaquette,
        # reverse the order of bits in the bitstring
        result = [np.array(list(reversed(key)), dtype=np.uint8) for key in input_counts]
        return result if len(result) > 1 else result[0]

    def get_sample(self) -> Tuple[List[Union[List[Any], Any]], Optional[List[None]]]:
        """Return the samples after a circuit run.

        Notes:
            This method assumes that the run method has already been called.
        """
        results = []
        for job in self._jobs:
            result_obj = job.result()
            res = self.convert_counts_to_arrays(result_obj.get_counts())
            results.append(res)

        num_jobs = len(self._jobs)
        if num_jobs == 1:
            results = results[0]

        erasure = [None] * num_jobs if num_jobs > 1 else None
        return results, erasure

    @property
    def is_completed(self) -> List[bool]:
        """Returns whether the jobs submitted by the device have been completed."""
        return [j.status() == JobStatus.DONE for j in self._jobs]
