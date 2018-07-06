"""Test the assemblies output by phyluce to ensure they are sane"""

import os
import shutil
import platform
import subprocess

from Bio import SeqIO

import pytest

import pdb

ROOTDIR = pytest.config.rootdir

@pytest.fixture(scope="module")
def o_dir(request):
    directory = os.path.join(ROOTDIR, "test")
    os.mkdir(directory)
    def clean():
        shutil.rmtree(directory)
    request.addfinalizer(clean)
    return directory

@pytest.fixture(scope="module")
def e_dir(request):
    directory = os.path.join(ROOTDIR, "phyluce", "tests", "test-results")
    return directory

@pytest.fixture(scope="module")
def o_dir(request):
    directory = os.path.join(ROOTDIR, "test")
    os.mkdir(directory)
    def clean():
        shutil.rmtree(directory)
    request.addfinalizer(clean)
    return directory


@pytest.fixture(scope="module")
def a_conf(request):
    return os.path.join(ROOTDIR, "phyluce/tests/test-conf/assembly-short.conf")


def get_contig_lengths_and_counts(contigs):
    with open(contigs) as contig_file:
        contig_count = 0
        contig_length = 0
        for seq in SeqIO.parse(contig_file, 'fasta'):
            contig_count += 1
            contig_length += len(seq)
    return contig_count, contig_length


def test_spades_assembly(o_dir, a_conf, e_dir):
    program = "bin/assembly/phyluce_assembly_assemblo_spades"
    cmd = [
        os.path.join(ROOTDIR, program),
        "--config",
        a_conf,
        "--cores",
        "1",
        "--output",
        "{}".format(os.path.join(o_dir, "spades")),
        "--log-path",
        o_dir
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stderr)
    observed_count, observed_length = get_contig_lengths_and_counts(
        os.path.join(o_dir, "spades", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    expected_count, expected_length = get_contig_lengths_and_counts(
        os.path.join(e_dir, "spades", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    assert observed_count == expected_count
    assert observed_length == expected_length

def test_abyss_assembly(o_dir, a_conf, e_dir):
    program = "bin/assembly/phyluce_assembly_assemblo_abyss"
    cmd = [
        os.path.join(ROOTDIR, program),
        "--config",
        a_conf,
        "--cores",
        "1",
        "--output",
        "{}".format(os.path.join(o_dir, "abyss")),
        "--abyss-se",
        "--log-path",
        o_dir
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    observed_count, observed_length = get_contig_lengths_and_counts(
        os.path.join(o_dir, "abyss", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    expected_count, expected_length = get_contig_lengths_and_counts(
        os.path.join(e_dir, "abyss", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    assert observed_count == expected_count
    assert observed_length == expected_length

def test_velvet_assembly(o_dir, a_conf, e_dir):
    program = "bin/assembly/phyluce_assembly_assemblo_velvet"
    cmd = [
        os.path.join(ROOTDIR, program),
        "--config",
        a_conf,
        "--cores",
        "1",
        "--output",
        "{}".format(os.path.join(o_dir, "velvet")),
        "--log-path",
        o_dir
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    observed_count, observed_length = get_contig_lengths_and_counts(
        os.path.join(o_dir, "velvet", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    expected_count, expected_length = get_contig_lengths_and_counts(
        os.path.join(e_dir, "velvet", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    assert observed_count == expected_count
    assert observed_length == expected_length


@pytest.mark.skipif(platform.system() == "Darwin", reason="requires linux")
def test_trinity_assembly(o_dir, a_conf, e_dir):
    program = "bin/assembly/phyluce_assembly_assemblo_trinity"
    cmd = [
        os.path.join(ROOTDIR, program),
        "--config",
        a_conf,
        "--cores",
        "1",
        "--output",
        "{}".format(os.path.join(o_dir, "trinity")),
        "--log-path",
        o_dir
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stderr)
    observed_count, observed_length = get_contig_lengths_and_counts(
        os.path.join(o_dir, "trinity", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    expected_count, expected_length = get_contig_lengths_and_counts(
        os.path.join(e_dir, "trinity", "contigs", "alligator_mississippiensis.contigs.fasta")
    )
    assert observed_count == expected_count
    assert observed_length == expected_length