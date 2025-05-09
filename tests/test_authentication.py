from pathlib import Path

import jwt as jwt


class TestAuthentication:
    test_internal_payload = {
        "accountId": "internal-user",
        "email": "user@communities.gov.uk",
        "fullName": "Internal User",
        "roles": ["COF_LEAD_ASSESSOR", "COF_ASSESSOR", "COF_COMMENTER"],
    }

    test_external_payload = {
        "accountId": "external-user",
        "email": "user@example.com",
        "fullName": "External User",
        "roles": ["COF_LEAD_ASSESSOR", "COF_ASSESSOR", "COF_COMMENTER"],
    }

    expected_valid_g_attributes = {
        "is_authenticated": True,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": "internal-user",
        "user": {
            "email": "user@communities.gov.uk",
            "full_name": "Internal User",
            "highest_role_map": {"COF": "LEAD_ASSESSOR"},
            "roles": ["COF_LEAD_ASSESSOR", "COF_ASSESSOR", "COF_COMMENTER"],
        },
    }

    expected_unauthenticated_g_attributes = {
        "is_authenticated": False,
        "logout_url": "https://authenticator/sessions/sign-out",
        "account_id": None,
    }

    def _create_valid_token(self, external=False):
        _test_private_key_path = str(Path(__file__).parent) + "/keys/rsa256/private.pem"
        with open(_test_private_key_path, mode="rb") as private_key_file:
            rsa256_private_key = private_key_file.read()
        payload = self.test_external_payload if external else self.test_internal_payload
        return jwt.encode(payload, rsa256_private_key, algorithm="RS256")

    def _create_invalid_token(self, external=False):
        _test_private_key_path = str(Path(__file__).parent) + "/keys/rsa256/private_invalid.pem"
        with open(_test_private_key_path, mode="rb") as private_key_file:
            rsa256_private_key = private_key_file.read()
        payload = self.test_external_payload if external else self.test_internal_payload
        return jwt.encode(payload, rsa256_private_key, algorithm="RS256")

    def test_login_required_redirects_to_signed_out_without_token(self, flask_test_client):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator
        WHEN a request is made without any "fsd-user-token" cookie
        THEN the route redirects to the authenticator /sessions/sign-out url
        :param flask_test_client:
        """
        mock_request = flask_test_client.get("/mock_login_required_route")

        assert mock_request.status_code == 302
        assert mock_request.location == "https://authenticator/sessions/sign-out"

    def test_login_required_redirects_to_signed_out_with_invalid_token(self, flask_test_client):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator
        WHEN a request is made with a correctly formatted
            but invalidly signed "fsd-user-token" cookie
        THEN the route redirects to the authenticator /sessions/sign-out url
        :param flask_test_client:
        """
        invalid_token = self._create_invalid_token()
        flask_test_client.set_cookie("fsd-user-token", invalid_token)
        mock_request = flask_test_client.get("/mock_login_required_route")

        assert mock_request.status_code == 302
        assert mock_request.location == "https://authenticator/sessions/sign-out"

    def test_login_required_sets_user_attributes_with_valid_token(self, flask_test_client):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
        THEN the route returns with the correct flask g variables set
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie("fsd-user-token", valid_token)
        mock_request = flask_test_client.get("/mock_login_required_route")
        assert mock_request.status_code == 200
        assert mock_request.json == self.expected_valid_g_attributes

    def test_login_required_roles_redirects_to_error_if_missing_roles(self, flask_test_client):
        """
        GIVEN a flask_test_client and route decorated with
            @login_required(roles_required=["ADMIN"]) decorator
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
            but without "ADMIN" in the roles param
        THEN the route redirects to the authenticator /sessions/sign-out url
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie("fsd-user-token", valid_token)
        mock_request = flask_test_client.get("/mock_login_required_admin_roles_route")
        assert mock_request.status_code == 302
        assert mock_request.location == "https://authenticator/service/user?roles_required=COF_ADMIN%7CCOF_TEST"

    def test_login_required_roles_redirects_to_error_with_source_app_if_missing_roles(self, flask_test_client):
        """
        GIVEN a flask_test_client and route decorated with
            @login_required(roles_required=["FSD_ADMIN"], return_app=SupportedApp.FUND_APPLICATION_BUILDER) decorator
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
            but without "FSD_ADMIN" in the roles param
        THEN the route redirects to the authenticator /service/user url with both roles_required and source_app
            parameters
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie("fsd-user-token", valid_token)
        mock_request = flask_test_client.get("/mock_login_required_admin_roles_with_return_app_route")
        assert mock_request.status_code == 302
        assert (
            mock_request.location
            == "https://authenticator/service/user?roles_required=FSD_ADMIN&source_app=fund-application-builder"
        )

    def test_login_required_roles_sets_user_attributes_if_user_has_roles(self, flask_test_client):
        """
        GIVEN a flask_test_client and route decorated with
            @login_required(roles_required=["COMMENTER"]) decorator
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
        THEN the route returns with the correct flask g variables set
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie("fsd-user-token", valid_token)
        mock_request = flask_test_client.get("/mock_login_required_roles_route")
        assert mock_request.status_code == 200
        assert mock_request.json == self.expected_valid_g_attributes

    def test_login_requested_sets_is_authenticated_to_false_with_no_token(self, flask_test_client):
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

    def test_login_requested_sets_user_attributes_with_valid_token(self, flask_test_client):
        """
        GIVEN a flask_test_client and
            route decorated with @login_requested decorator
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
        THEN the route returns with the correct flask g variables set
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie("fsd-user-token", valid_token)
        mock_request = flask_test_client.get("/mock_login_requested_route")
        assert mock_request.status_code == 200
        assert mock_request.json == self.expected_valid_g_attributes

    def test_login_required_roles_debuggable_in_development(self, flask_test_development_client):
        """
        GIVEN a flask_test_client and route decorated with
            @login_required(roles_required=["ADMIN"]) decorator
            and env vars of:
                FLASK_ENV = 'development'
                DEBUG_USER_ROLE = "ADMIN"
        WHEN a request is made without a valid fsd_user_token cookie
        THEN the route is still accessible
        :param flask_test_client:
        """
        flask_test_development_client.set_cookie("fsd-user-token", "")
        mock_request = flask_test_development_client.get("/mock_login_required_admin_roles_route")
        assert mock_request.status_code == 200

    def test_login_required_roles_debuggable_but_still_requires_roles(self, flask_test_development_client):
        """
        GIVEN a flask_test_client and route decorated with
            @login_required(roles_required=["COMMENTER"]) decorator
            and env vars of:
                FLASK_ENV = 'development'
                DEBUG_USER_ROLE = "ADMIN"
        WHEN a request is made without a valid fsd_user_token cookie
        THEN the route redirects to the authenticator /sessions/sign-out url
        :param flask_test_client:
        """
        flask_test_development_client.set_cookie("fsd-user-token", "")
        mock_request = flask_test_development_client.get("/mock_login_required_roles_route")
        assert mock_request.status_code == 302
        assert mock_request.location == "https://authenticator/service/user?roles_required=COF_COMMENTER"

    def test_login_required_with_return_app_redirects_to_signed_out_without_token(self, flask_test_client):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator with the "return_app" parameter set to "post-award-frontend"
        WHEN a request is made without any "fsd-user-token" cookie
        THEN the route redirects to the authenticator /sessions/sign-out url with correct return_app query param
        :param flask_test_client:
        """
        mock_request = flask_test_client.get("/mock_login_requested_return_app_route")

        assert mock_request.status_code == 302
        assert (
            mock_request.location
            == "https://authenticator/sessions/sign-out?return_app=post-award-frontend&return_path=%2Fmock_login_requested_return_app_route"  # noqa: E501
        )

    def test_login_required_with_return_app_redirects_to_signed_out_with_invalid_token(self, flask_test_client):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator with the "return_app" parameter set to "post-award-frontend"
        WHEN a request is made with a correctly formatted
            but invalidly signed "fsd-user-token" cookie
        THEN the route redirects to the authenticator /sessions/sign-out url with correct return_app query param
        :param flask_test_client:
        """
        invalid_token = self._create_invalid_token()
        flask_test_client.set_cookie("fsd-user-token", invalid_token)
        mock_request = flask_test_client.get("/mock_login_requested_return_app_route")

        assert mock_request.status_code == 302
        assert (
            mock_request.location
            == "https://authenticator/sessions/sign-out?return_app=post-award-frontend&return_path=%2Fmock_login_requested_return_app_route"  # noqa: E501
        )

    def test_login_required_with_return_app_return_path_retains_query_string(self, flask_test_client):
        mock_request = flask_test_client.get("/mock_login_requested_return_app_route?foo=bar")

        assert mock_request.status_code == 302
        assert (
            mock_request.location
            == "https://authenticator/sessions/sign-out?return_app=post-award-frontend&return_path=%2Fmock_login_requested_return_app_route%3Ffoo%3Dbar"  # noqa: E501
        )

    def test_login_required_with_return_app_sets_user_attributes_with_valid_token(self, flask_test_client):
        """
        GIVEN a flask_test_client and
            route decorated with @login_required decorator with the "return_app" parameter set to "post-award-frontend"
        WHEN a request is made with a correctly formatted
            and signed "fsd-user-token" cookie
        THEN the route returns with the g variable "logout_url" set correctly
        :param flask_test_client:
        """
        valid_token = self._create_valid_token()
        flask_test_client.set_cookie("fsd-user-token", valid_token)
        mock_request = flask_test_client.get("/mock_login_requested_return_app_route")
        assert mock_request.status_code == 200
        assert (
            mock_request.json["logout_url"]
            == "https://authenticator/sessions/sign-out?return_app=post-award-frontend&return_path=%2Fmock_login_requested_return_app_route"  # noqa: E501
        )

    def test_check_internal_user_allows_unauthenticated(self, flask_test_check_internal_user_client):
        """
        GIVEN no authentication token is provided
        WHEN requesting the route decorated with @check_internal_user
        THEN it should return 200 since unauthenticated users are allowed.
        """
        response = flask_test_check_internal_user_client.get("/mock_check_internal_user_route")
        assert response.status_code == 200
        assert response.json == {"status": "ok"}

    def test_check_internal_user_allows_internal_domain(self, flask_test_check_internal_user_client):
        """
        GIVEN a valid JWT with an internal domain email (e.g. '@communities.gov.uk')
        WHEN requesting the route
        THEN it should return 200 since internal domain users are allowed.
        """
        token = self._create_valid_token(external=False)
        flask_test_check_internal_user_client.set_cookie("fsd-user-token", token)

        response = flask_test_check_internal_user_client.get("/mock_check_internal_user_route")
        assert response.status_code == 200
        assert response.json == {"status": "ok"}

    def test_check_internal_user_denies_external_domain(self, flask_test_check_internal_user_client):
        """
        GIVEN a valid JWT with a non-internal domain email
        WHEN requesting the route
        THEN it should return 403 since external domain users are not allowed.
        """
        token = self._create_valid_token(external=True)
        flask_test_check_internal_user_client.set_cookie("fsd-user-token", token)

        response = flask_test_check_internal_user_client.get("/mock_check_internal_user_route")
        assert response.status_code == 403
