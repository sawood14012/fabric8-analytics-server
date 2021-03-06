"""Test Case for User Management Utilities."""
import pytest
from bayesian.utility import user_utils
from f8a_utils.user_token_utils import UserStatus


@pytest.fixture
def create_user(rdb):
    """Fixture that creates a user which is used on other tests."""
    assert rdb
    user_utils.create_or_update_user('03ec8318-08ed-4aeb', 'abc', 'SNYK')


@pytest.mark.usefixtures('rdb')
class TestUserUtils:
    """Test cases for user management utilities."""

    @pytest.mark.usefixtures('create_user')
    def test_get_user(self):
        """Test case for get user."""
        user = user_utils.get_user('03ec8318-08ed-4aeb')
        assert user.snyk_api_token == 'abc'

    @pytest.mark.usefixtures('create_user')
    def test_get_user_not_found(self):
        """Test case for get user not found."""
        assert user_utils.get_user('uuid') is None

    def test_create_user(self):
        """Test case for create user."""
        user_utils.create_or_update_user('03ec8318-08ed-4aeb', 'abc', 'SNYK')
        assert user_utils.get_user('03ec8318-08ed-4aeb').snyk_api_token == 'abc'
        assert user_utils.get_user('03ec8318-08ed-4aeb').status == UserStatus.REGISTERED.name

    @pytest.mark.usefixtures('create_user')
    def test_update_user(self):
        """Test case for update user."""
        assert user_utils.get_user('03ec8318-08ed-4aeb').snyk_api_token == 'abc'
        user_utils.create_or_update_user('03ec8318-08ed-4aeb', 'def', 'SNYK')
        assert user_utils.get_user('03ec8318-08ed-4aeb').snyk_api_token == 'def'
        assert user_utils.get_user('03ec8318-08ed-4aeb').status == UserStatus.REGISTERED.name
