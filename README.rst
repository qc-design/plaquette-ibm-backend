``plaquette-ibm-backend-``: connecting ``plaquette`` to IBM Quantum
===================================================================

``plaquette-ibm-backend`` is an easy to install plugin that allows using IBM Quantum
remote systems and simulators with `plaquette <https://docs.plaquette.design/>`_.

Installation
------------

``plaquette-ibm-backend`` is a pure Python package, so it can be easily installed via
``pip``::

   pip install plaquette-ibm-backend


Example
-------

First, authenticate to IBM Quantum by providing a token. This can be done for
example via

.. code-block:: python

    from qiskit_ibm_provider import IBMProvider
    IBMProvider.save_account("<Your token>")

.. note::

    To specify a custom hub/group/project, the ``instance`` argument can be
    passed to ``save_account``.

For further ways of authentication refer to the IBM Quantum and Qiskit documentation.

Once the account has been saved, a quantum ciruict generated from a code in
plaquette can be run easily on a remote simulator provided by IBM by specifying
the ``"ibm"`` backend and the name of an IBM system:

.. code-block:: python

    import plaquette
    from plaquette.circuit import Circuit
    from plaquette.codes import LatticeCode
    from plaquette.errors import QubitErrorsDict
    from plaquette.circuit.generator import generate_qec_circuit

    # Select a code we'd like to simulate
    code = LatticeCode.make_repetition(n_rounds=1, size=3)

    # Generate the quantum circuit of the code
    logical_operator = "X"
    circuit = generate_qec_circuit(code, {}, {}, logical_operator)

    # Select an IBM Quantum system or simulator by specifying its name during
    # device creation
    system_name = "simulator_stabilizer"
    dev = plaquette.Device("ibm", system_name=system_name)
    dev.run(circuit)
    samples, _ = dev.get_sample()

.. code-block:: pycon

    >>> samples
    array([0, 1, 1, 1, 0, 0, 0, 0, 0, 0], dtype=uint8)


.. important::

   Not *all* circuits supported by ``plaquette`` can be run on IBM Quantum
   systems and simulators, as some ``plaquette`` instructions cannot be
   converted to ``OpenQASM 3.0`` (e.g., any circuit with "error instructions"
   cannot be converted). When creating a ``plaquette`` device with an IBM
   backend, the plugin will leave unsupported instructions out of the circuit
   during conversion to ``OpenQASM``.

Need help? Want to contribute?
------------------------------

``plaquette-ibm`` is under heavy development, so it might have some rough corners that need
polishing. If you encounter something you think (or the docs say) should work but does
not, just open an `issue <https://github.com/qc-design/plaquette-ibm/issues/new>`_
or, if you also want to share a solution, a
`pull request <https://github.com/qc-design/plaquette-ibm/compare>`_! See
our `development standard <https://docs.plaquette.design/dev/index.html>`_ to
have an idea of how to match your suggestions to the codebase.

Want to simply share feedback or you're unsure how to do something? Open a new
`discussion <https://github.com/qc-design/plaquette/discussions/new/choose>`_!
