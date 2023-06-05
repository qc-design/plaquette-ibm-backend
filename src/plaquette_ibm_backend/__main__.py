# Copyright 2023, QC Design GmbH and the plaquette-ibm contributors
# SPDX-License-Identifier: Apache-2.0
"""Entry-point module to recover plaquette-ibm's version quickly."""
import plaquette_ibm_backend

print(f"plaquette-ibm-{plaquette_ibm_backend.__version__}")
