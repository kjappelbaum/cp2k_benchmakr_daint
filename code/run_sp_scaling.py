# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""
This submits the scaling test, i.e. the same calculation on a different number of nodes. 
Repository aiida.out in c.get_retrieved_node()._repository._get_base_folder().abspath, 
where c is the calculation node which the workchain produces
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
@click.option("--run_test", is_flag=True, help="Actually submit calculation")
def main(codelabel, run_test):
    try:
        code = Code.get_from_string(codelabel)
    except NotExistent:
        print("The code '{}' does not exist".format(codelabel))
        sys.exit(1)

    allstructures = [
        "/home/kevin/Dropbox (LSMO)/proj61_metal_channels_shared/8_benchmark_daint/structures/dft_opt/NAVJAW.cif"
    ]

    for num_nodes in [1, 2, 4, 8, 12, 16, 32]:
        for s in allstructures:
            cif = CifData(file=s)
            name = Path(s).stem
            structure = cif.get_structure()
            structure.label = name

            structure.store()

            parameters = Dict(dict={})
            options = {
                "resources": {"num_machines": num_nodes, "num_cores_per_mpiproc": 1},
                "max_wallclock_seconds": 1 * 60 * 60,
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
                "metadata": {"label": "scaling_test_" + str(num_nodes)},
            }

            if run_test:
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
