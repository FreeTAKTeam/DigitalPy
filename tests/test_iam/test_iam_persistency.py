from digitalpy.core.IAM.persistence.user import User
from tests.testing_utilities.facade_utilities import initialize_test_environment, initialize_facade
from digitalpy.core.IAM.configuration import iam_constants

iam_constants.DB_PATH = "sqlite+pysqlite:///:memory:"

def test_default_admin_instantiation():
    request, response, _ = initialize_test_environment()
    iam_facade = initialize_facade("digitalpy.core.IAM.IAM_facade.IAM", request, response)    
    request.set_value("cn", "Administrator")
    iam_facade.execute("get_user_by_cn")
    admin_user: User = response.get_value("users")[0]
    assert admin_user is not None
    assert admin_user.CN == "Administrator"
    assert admin_user.callsign == "Administrator"

    assert admin_user.system_user is not None
    assert admin_user.system_user.name == "Administrator"
    assert admin_user.system_user.token == "admin"
    assert admin_user.system_user.password == "admin"
    assert admin_user.system_user.device_type == "admin"
    assert admin_user.system_user.certificate_package_name == "admin"

    assert len(admin_user.system_user.system_user_groups) == 2
    if admin_user.system_user.system_user_groups[0].system_group.name == "admin_users":
        assert admin_user.system_user.system_user_groups[1].system_group.name == "authenticated_users"
    elif admin_user.system_user.system_user_groups[1].system_group.name == "admin_users":
        assert admin_user.system_user.system_user_groups[0].system_group.name == "authenticated_users"
    else:
        assert False

def test_default_anonymous_instantiation():
    request, response, _ = initialize_test_environment()
    iam_facade = initialize_facade("digitalpy.core.IAM.IAM_facade.IAM", request, response)    
    request.set_value("cn", "Anonymous")
    iam_facade.execute("get_user_by_cn")
    anonymous_user: User = response.get_value("users")[0]
    assert anonymous_user is not None
    assert anonymous_user.CN == "Anonymous"
    assert anonymous_user.callsign == "Anonymous"

    assert anonymous_user.system_user is not None
    assert anonymous_user.system_user.name == "Anonymous"
    assert anonymous_user.system_user.token == "anonymous"
    assert anonymous_user.system_user.password == "anonymous"
    assert anonymous_user.system_user.device_type == "anonymous"
    assert anonymous_user.system_user.certificate_package_name == "anonymous"

    assert len(anonymous_user.system_user.system_user_groups) == 1
    assert anonymous_user.system_user.system_user_groups[0].system_group.name == "unauthenticated_users"