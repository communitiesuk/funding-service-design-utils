from pathlib import Path

import jwt as jwt


class TestAuthentication:

    test_payload = {
        "accountId": "test-user",
        "email": "test@example.com",
        "fullName": "Test User",
        "roles": ["LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"],
    }
    expected_valid_g_attributes = {
        "is_authenticated": True,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": "test-user",
        "user": {
            "email": "test@example.com",
            "full_name": "Test User",
            "highest_role": "LEAD_ASSESSOR",
            "roles": ["LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"],
        },
    }

    expected_unauthenticated_g_attributes = {
        "is_authenticated": False,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": None,
        "user": None,
    }

    def _create_valid_token(self):

        _test_private_key_path = (
            str(Path(__file__).parent) + "/keys/rsa256/private.pem"
        )
        with open(_test_private_key_path, mode="rb") as private_key_file:
            rsa256_private_key = private_key_file.read()

            return jwt.encode(
                self.test_payload, rsa256_private_key, algorithm="RS256"
            )

    def _create_invalid_token(self):

        _test_private_key_path = (
            str(Path(__file__).parent) + "/keys/rsa256/private_invalid.pem"
        )
        with open(_test_private_key_path, mode="rb") as private_key_file:
            rsa256_private_key = private_key_file.read()

            return jwt.encode(
                self.test_payload, rsa256_private_key, algorithm="RS256"
            )

    def test_login_required_redirects_to_signed_out_without_token(
        self, flask_test_client
    ):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator
        WHEN a request is made without any "fsd-user-token" cookie
        THEN the route redirects to the authenticator /sessions/sign-out url
        :param flask_test_client:
        """
        mock_request = flask_test_client.get("/mock_login_required_route")

        assert mock_request.status_code == 302
        assert (
            mock_request.location == "https://authenticator/sessions/sign-out"
        )

    def test_login_required_redirects_to_signed_out_with_invalid_token(
        self, flask_test_client
    ):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator
        WHEN a request is made with a correctly formatted
            but invalidly signed "fsd-user-token" cookie
        THEN the route redirects to the authenticator /sessions/sign-out url
        :param flask_test_client:
        """
        invalid_token = self._create_invalid_token()
        flask_test_client.set_cookie(
            "localhost", "fsd-user-token", invalid_token
        )
        mock_request = flask_test_client.get("/mock_login_required_route")

        assert mock_request.status_code == 302
        assert (
            mock_request.location == "https://authenticator/sessions/sign-out"
        )

    def test_login_required_sets_user_attributes_with_valid_token(
        self, flask_test_client
    ):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
        THEN the route returns with the correct flask g variables set
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie(
            "localhost", "fsd-user-token", valid_token
        )
        mock_request = flask_test_client.get("/mock_login_required_route")
        assert mock_request.status_code == 200
        assert mock_request.json == self.expected_valid_g_attributes

    def test_login_requested_sets_is_authenticated_to_false_with_no_token(
        self, flask_test_client
    ):
        """
        GIVEN a flask_test_client and
            route decorated with @login_requested decorator
        WHEN a request is without any "fsd-user-token" cookie
        THEN the route returns with flask g.is_authenticated == False
        :param flask_test_client:
        """
        mock_request = flask_test_client.get("/mock_login_requested_route")
        assert mock_request.status_code == 200
        assert mock_request.json == self.expected_unauthenticated_g_attributes

    def test_login_requested_sets_user_attributes_with_valid_token(
        self, flask_test_client
    ):
        """
        GIVEN a flask_test_client and
            route decorated with @login_requested decorator
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
        THEN the route returns with the correct flask g variables set
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie(
            "localhost", "fsd-user-token", valid_token
        )
        mock_request = flask_test_client.get("/mock_login_requested_route")
        assert mock_request.status_code == 200
        assert mock_request.json == self.expected_valid_g_attributes
