import contextlib
import glob
import os
import pkg_resources

from pip._internal import main as pip_main
from wheel import wheelfile

from piprules import namespace_pkgs, util


class Error(Exception):

    """Base exception for the wheels module"""


def download(dest_directory, requirements_file_path, *extra_args):
    with _add_pip_import_paths_to_pythonpath():
        pip_main(
            args=["wheel", "-w", dest_directory, "-r", requirements_file_path]
            + list(extra_args)
        )


@contextlib.contextmanager
def _add_pip_import_paths_to_pythonpath():
    import pip
    import setuptools
    import wheel

    import_paths = [util.get_import_path_of_module(m) for m in [pip, setuptools, wheel]]
    with util.prepend_to_pythonpath(import_paths):
        yield


def find_all(directory):
    for matching_path in glob.glob("{}/*.whl".format(directory)):
        yield matching_path


def unpack(wheel_path, dest_directory):
    # TODO(): don't use unsupported wheel library
    with wheelfile.WheelFile(wheel_path) as wheel_file:
        distribution_name = wheel_file.parsed_filename.group("name")
        library_name = util.normalize_distribution_name(distribution_name)
        package_directory = os.path.join(dest_directory, library_name)
        wheel_file.extractall(package_directory)
        namespace_pkgs.setup_namespace_pkg_compatibility(package_directory)
    try:
        return next(pkg_resources.find_distributions(package_directory))
    except StopIteration:
        raise DistributionNotFoundError(package_directory)


class DistributionNotFoundError(Error):
    def __init__(self, package_directory):
        super(DistributionNotFoundError, self).__init__()
        self.package_directory = package_directory

    def __str__(self):
        return "Could not find in Python distribution in directory {}".format(
            self.package_directory
        )
