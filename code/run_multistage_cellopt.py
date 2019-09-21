# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""
This submits the multistage DFT optimization workchain
/home/kevin/Dropbox/proj61_metal_channels_shared/8_benchmark_daint/structures
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

from aiida.engine import submit
from aiida.orm import Code, Dict, StructureData
from aiida.common import NotExistent
from aiida_cp2k.workchains import Cp2kMultistageWorkChain
from aiida.plugins import DataFactory

CifData = DataFactory("cif")


@click.command("cli")
@click.argument("codelabel")
# @click.argument("structuredir")
@click.option("--run", is_flag=True, help="Actually submit calculation")
def main(codelabel, run):
    try:
        code = Code.get_from_string(codelabel)
    except NotExistent:
        print("The code '{}' does not exist".format(codelabel))
        sys.exit(1)

    allstructures = [
        "/home/kevin/Dropbox (LSMO)/proj61_metal_channels_shared/8_benchmark_daint/structures/from_curated_mofs/UTEWOG.cif"
    ]

    for s in allstructures:
        print("submitting mulitstage cellopt on {}".format(s))
        cif = CifData(file=s)
        name = Path(s).stem
        structure = cif.get_structure()
        structure.label = name

        structure.store()
        parameters = Dict(dict={})
        options = {
            "resources": {"num_machines": 1},
            "max_wallclock_seconds": 15 * 60 * 60,
        }
        inputs = {
            "protocol_tag": Str("standard"),
            "cp2k_base": {
                "cp2k": {
                    "structure": structure,
                    "parameters": parameters,
                    "code": code,
                    "metadata": {"options": options},
                }
            },
        }

        if run:
            submit(Cp2kMultistageWorkChain, **inputs)
        else:
            print("Generating test input ...")
            inputs["base"]["cp2k"]["metadata"]["dry_run"] = True
            inputs["base"]["cp2k"]["metadata"]["store_provenance"] = False
            run(Cp2kMultistageWorkChain, **inputs)
            print("Submission test successful")
            print("In order to actually submit, add '--run'")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
