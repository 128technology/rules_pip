load("//:python.bzl", "PYTHON2", "PYTHON3")
load("//tools/pytest:rules.bzl", "pytest_test")

pytest_test(
    name = "dependency_deduplication_test_2",
    src = "dependency_deduplication_test.py",
    python_version = 2,
    deps = ["@pip2//isort"],
)

pytest_test(
    name = "dependency_deduplication_test_3",
    src = "dependency_deduplication_test.py",
    python_version = 3,
    deps = ["@pip3//isort"],
)

pytest_test(
    name = "mock_test_2",
    src = "mock_test.py",
    python_version = 2,
    deps = ["@pip2//pytest_mock"],
)

pytest_test(
    name = "mock_test_3",
    src = "mock_test.py",
    python_version = 3,
    deps = ["@pip3//pytest_mock"],
)

pytest_test(
    name = "pathlib_test_2",
    src = "pathlib_test.py",
    python_version = 2,
    deps = ["@pip2//pathlib2"],
)

pytest_test(
    name = "pathlib_test_3",
    src = "pathlib_test.py",
    python_version = 3,
)

pytest_test(
    name = "pyyaml_test_2",
    src = "pyyaml_test.py",
    python_version = 2,
    deps = ["@pip2//pyyaml"],
)

pytest_test(
    name = "pyyaml_test_3",
    src = "pyyaml_test.py",
    python_version = 3,
    deps = ["@pip3//pyyaml"],
)

pytest_test(
    name = "namespace_pkgs_test",
    src = "namespace_pkgs_test.py",
    python_version = 3,
    deps = [
        "@pip3_internal//azure_mgmt_compute",
        "@pip3_internal//azure_mgmt_resource",
    ],
)

genrule(
    name = "pyang2_script",
    srcs = ["@pip2//pyang/scripts:pyang"],
    outs = ["pyang2.py"],
    cmd = "$(location //src/bin:replace_shebang) $< $@ %s" % PYTHON2,
    tools = ["//src/bin:replace_shebang"],
)

py_binary(
    name = "pyang2",
    srcs = [":pyang2_script"],
    deps = ["@pip2//pyang"],
)

genrule(
    name = "test-yin-2",
    srcs = ["@pip2//pyang/data/share/yang/modules/ietf:ietf-yang-metadata.yang"],
    outs = ["ietf-yang-metadata-2.yin"],
    cmd = "$(location :pyang2) -f yin -o $@ $<",
    tools = [":pyang2"],
)

genrule(
    name = "pyang3_script",
    srcs = ["@pip3//pyang/scripts:pyang"],
    outs = ["pyang3.py"],
    cmd = "$(location //src/bin:replace_shebang) $< $@ %s" % PYTHON3,
    tools = ["//src/bin:replace_shebang"],
)

py_binary(
    name = "pyang3",
    srcs = [":pyang3_script"],
    deps = ["@pip3//pyang"],
)

genrule(
    name = "test-yin-3",
    srcs = ["@pip3//pyang/data/share/yang/modules/ietf:ietf-yang-metadata.yang"],
    outs = ["ietf-yang-metadata-3.yin"],
    cmd = "$(location :pyang3) -f yin -o $@ $<",
    tools = [":pyang3"],
)

pytest_test(
    name = "data_test",
    src = "data_test.py",
    data = [
        "ietf-yang-metadata.yin",
        ":test-yin-2",
        ":test-yin-3",
    ],
    python_version = 3,
)
