# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""
This submits a water single point to test the setup.
"""

from __future__ import print_function
from __future__ import absolute_import
import os
import click

import sys
import ase.build
from pathlib import Path
import os
from glob import glob

from aiida.engine import submit, run
from aiida.orm import Code, Dict, StructureData
from aiida.common import NotExistent
from aiida_cp2k.workchains import Cp2kMultistageWorkChain
from aiida.plugins import DataFactory

CifData = DataFactory("cif")
StructureData = DataFactory("structure")


@click.command("cli")
@click.argument("codelabel")
@click.option("--run_test", is_flag=True, help="Actually submit calculation")
def main(codelabel, run_test):
    try:
        code = Code.get_from_string(codelabel)
    except NotExistent:
        print("The code '{}' does not exist".format(codelabel))
        sys.exit(1)

    atoms = ase.build.molecule("H2O")
    atoms.center(vacuum=2.0)
    structure = StructureData(ase=atoms)

    parameters = Dict(dict={})
    options = {
        "resources": {"num_machines": 1, "num_cores_per_mpiproc": 1},
        "max_wallclock_seconds": int(0.5 * 60 * 60),
    }
    inputs = {
        "protocol_tag": Str("sp"),
        "cp2k_base": {
            "cp2k": {
                "structure": structure,
                "parameters": parameters,
                "code": code,
                "metadata": {"options": options},
            }
        },
        "metadata":{
            "label": "testing_daint_setup"
        }
    }

    if run_test:
        submit(Cp2kMultistageWorkChain, **inputs)
    else:
        print("Generating test input ...")
        inputs["cp2k_base"]["cp2k"]["metadata"]["dry_run"] = True
        inputs["cp2k_base"]["cp2k"]["metadata"]["store_provenance"] = False
        run(Cp2kMultistageWorkChain, **inputs)
        print("Submission test successful")
        print("In order to actually submit, add '--run'")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
