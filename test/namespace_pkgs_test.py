def test_namespace_pkg_import():
    from azure.mgmt import resource, compute

    # these not throwing attribute errors will verify that the import was successful
    resource.version
    compute.version
