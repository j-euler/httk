#!/usr/bin/env python

import os, sys
import re
import numpy as np
import httk, httk.iface.vasp_if
from httk.iface.vasp_if import get_elastic_constants
import httk.db
from httk.core import HttkObject, FracVector, FracScalar
from httk.atomistic import Structure, UnitcellStructure
from httk.atomistic.results.elasticresult import Result_ElasticResult
import httk.task
import subprocess
import glob
import bz2
import json
import zipfile
import shutil
import atexit
import signal

def handle_exit():
    shutil.rmtree('Runs_finished', ignore_errors=True)

def make_database(db_name):
    try:
        os.remove(db_name)
    except:
        pass

    zip = zipfile.ZipFile('Runs_finished.zip')
    zip.extractall()

    backend = httk.db.backend.Sqlite(db_name)
    store = httk.db.store.SqlStore(backend)
    reader = httk.task.reader('./', 'Runs_finished/', 'Total energy and elastic constants')

    index = 1
    for rundir, computation in reader:
        root = os.path.join(rundir, '..')
        # Check whether the calculation included atomic relaxations or not:
        isif_found = False
        with open(os.path.join(root, 'INCAR.relax')) as tmp:
            lines = tmp.readlines()
            for l in lines:
                isif = re.search("^[^#]*ISIF\s*=\s*(\d)", l)
                if isif is not None:
                    isif = int(isif.groups()[0])
                    isif_found = True
                    break

        if not isif_found:
            sys.exit("ERROR: Atomic relaxation information could not be determined for rundir: {}".format(rundir))

        initial_struct = httk.load(os.path.join(root, 'POSCAR'))
        struct = httk.load(os.path.join(rundir, "CONTCAR.relax-final"))

        # Handle tags
        tags = eval(initial_struct.get_tags()['comment'].value)
        initial_struct._tags = None
        initial_struct._codependent_data = []
        struct._tags = None
        struct._codependent_data = []
        for tag in tags:
            tmp = re.search("^\(Tag\)\s(.*):\s(.*)", tag)
            if tmp is not None:
                initial_struct.add_tag(tmp.groups()[0], tmp.groups()[1])
                struct.add_tag(tmp.groups()[0], tmp.groups()[1])

        # Check whether elastic constants were calculated:
        cij, sij, elas_dict, cij_nosym = get_elastic_constants(rundir)

        atomic_relaxations = struct.get_tag('atomic_relaxations').value
        if atomic_relaxations == 'False':
            atomic_relaxations = False
        elif atomic_relaxations == 'True':
            atomic_relaxations = True

        outcar = httk.iface.vasp_if.read_outcar(os.path.join(rundir, "OUTCAR.cleaned.relax-final"))
        result = Result_ElasticResult(
                float(outcar.final_energy),
                computation, initial_struct, struct,
                cij, cij_nosym, sij, elas_dict['K_V'],
                elas_dict['K_R'], elas_dict['K_VRH'],
                elas_dict['G_V'], elas_dict['G_R'],
                elas_dict['G_VRH'], elas_dict['mu_VRH'],
                elas_dict['E_VRH'], atomic_relaxations,
                "", # walltimes
                "", # rundir
                "", # material_id
                )

        print("{0:3} Processed outcar: {1:10}".format(index, initial_struct.formula))

        store.save(result)
        index += 1

        print("Elastic tensor:")
        for row in cij:
            print("{0:3.0f} {1:3.0f} {2:3.0f} {3:3.0f} {4:3.0f} {5:3.0f}".format(*row))

    store.commit()

if __name__ == '__main__':
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    db_name = 'elastic_constants.sqlite'
    make_database(db_name)
    shutil.rmtree('Runs_finished', ignore_errors=True)