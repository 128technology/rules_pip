import argparse
import glob
import os
import subprocess
import sys
import textwrap
from wheel import wheelfile


def main():
    print('executing create_wheels_repo')
    args = parse_args()
    download_wheels(args.requirements, args.repository_directory)
    expand_wheels_into_bazel_packages(args.repository_directory)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("requirements")
    parser.add_argument("repository_directory")

    return parser.parse_args()


def download_wheels(requirements_file_path, repository_directory):
    pip("wheel", "-r", requirements_file_path, "-w", repository_directory)


def pip(*args):
    execute_python_module("pip", *args)


def execute_python_module(module_name, *args):
    subprocess.check_call([sys.executable, "-m", module_name] + list(args))


def expand_wheels_into_bazel_packages(repository_directory):
    for wheel_path in find_wheels(repository_directory):
        unpack_wheel_into_bazel_package(wheel_path, repository_directory)


def find_wheels(directory):
    for matching_path in glob.glob("{}/*.whl".format(directory)):
        yield matching_path


def unpack_wheel_into_bazel_package(wheel_path, repository_directory):
    wheel_name, package_directory = unpack_wheel(
        wheel_path,
        repository_directory
    )

    create_bazel_build_file(wheel_name, package_directory)


def unpack_wheel(wheel_path, repository_directory):
    with wheelfile.WheelFile(wheel_path) as wheel_file:
        name = normalize_wheel_name(wheel_file.parsed_filename.group('name'))
        package_directory = os.path.join(repository_directory, name)
        wheel_file.extractall(package_directory)

    return name, package_directory


def normalize_wheel_name(name):
    return name.lower()


def create_bazel_build_file(wheel_name, package_directory):
    path = os.path.join(package_directory, "BUILD")

    contents = textwrap.dedent("""
        py_library(
            name = "{name}",
            srcs = glob(["**/*.py"]),
            data = glob(
                ["**/*"],
                exclude = ["**/*.py", "BUILD", "WORKSPACE", "*.whl.zip"]
            ),
            imports = ["."],
            visibility = ["//visibility:public"],
        )
    """).lstrip().format(name=wheel_name)

    with open(path, mode='w') as build_file:
        build_file.write(contents)


if __name__ == "__main__":
    main()
