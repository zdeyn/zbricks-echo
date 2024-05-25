# tests/test_auth_routes.py
import pytest

from unittest.mock import MagicMock
from flask import Flask, make_response
from rich import print
from flask.testing import FlaskClient
from pytest_mock import MockFixture

# from zbricks.auth.blueprint import fetch_profile_data, find_or_create_user

class Test_Auth_Routes_Login:

    def test_login_redirects_to_discord(self, client : FlaskClient):
        """Test that the login page redirects to discord.com"""

        response = client.get('/auth/login')

        # Check if the status code is 302, which is standard for a redirect
        assert response.status_code == 302

        # Check if the Location header contains the URL for Discord's OAuth
        assert 'discord.com/api/oauth2/authorize' in response.headers['Location']

        # Check for the presence of client_id in the redirect URL
        assert 'client_id' in response.headers['Location']

class Test_Auth_Routes_Authorize:

    def test_calls_all_the_things(self, 
                                    app : Flask,
                                    client : FlaskClient, 
                                    mocker : MockFixture, 
                                    mock_discord : MagicMock,
                                ):
        """Test that the authorize route calls helper functions"""

        fake_token = {'access_token': 'fake_access_token', 'refresh_token': 'fake_refresh_token'}
        mock_discord.authorize_access_token.return_value = fake_token

        fake_profile = {
            "id": "806509581370523659",
            "username": "zdeyn",
            "global_name": "zdeyn",
            "email": "i.am.zdeyn@gmail.com",
            "avatar": "49ad4de837ec35240df48773ed1249e5",
            "banner_color": "#9c13cd",
            "discriminator": "0",
            "locale": "en-GB",
            "verified": True
        }
        mock_discord.get.return_value = fake_profile

        # mock_fetch_profile_data = mocker.patch("zbricks.auth.blueprint.fetch_profile_data", return_value=fake_profile)

        # mock_create_access_token = mocker.patch("zbricks.auth.blueprint.create_access_token", return_value="fake_access_token")

        # Make a request to the authorize route
        response = client.get('/auth/authorize')

        db = app.extensions.get('sqlalchemy')
        
        # mock_fetch_profile_data.assert_called_once_with(mock_discord)
        # mock_find_or_create_user.assert_called_once_with(db, fake_profile)
        # mock_create_access_token.assert_called_once()


    def test_authorizes_access_token(self, client : FlaskClient, mock_discord : MagicMock):
        """Test that the authorize route calls authorize_access_token"""

        fake_token = {'access_token': 'fake_access_token', 'refresh_token': 'fake_refresh_token'}
        mock_discord.authorize_access_token.return_value = fake_token

        fake_profile = {
            "avatar": "49ad4de837ec35240df48773ed1249e5",
            "banner_color": "#9c13cd",
            "discriminator": "0",
            "email": "i.am.zdeyn@gmail.com",
            "global_name": "zdeyn",
            "id": "806509581370523659",
            "locale": "en-GB",
            "username": "zdeyn",
            "verified": True
        }
        mock_discord.get.return_value = fake_profile

        # Make a request to the authorize route
        response = client.get('/auth/authorize')

        # Check if the authorize_access_token function was called
        mock_discord.authorize_access_token.assert_called_once()
        mock_discord.get.assert_called_once_with('users/@me')
    
    # def test_obtains_profile(self, client : FlaskClient, mock_discord : MagicMock):
    #     """Test that the authorize route fetches the user's profile"""

    #     fake_token = {'access_token': 'test_token'}
    #     mock_discord.authorize_access_token.return_value = fake_token

    #     fake_profile = {
    #         "avatar": "49ad4de837ec35240df48773ed1249e5",
    #         "banner_color": "#9c13cd",
    #         "discriminator": "0",
    #         "email": "i.am.zdeyn@gmail.com",
    #         "global_name": "zdeyn",
    #         "id": "806509581370523659",
    #         "locale": "en-GB",
    #         "username": "zdeyn",
    #         "verified": True
    #     }
    #     mock_discord.get.return_value = make_response(fake_profile, 200)

    #     # Make a request to the authorize route
    #     response = client.get('/auth/authorize')

    #     # Check if the discord api was accessed to fetch the profile data
    #     mock_discord.get.assert_called_once_with('users/@me', token = fake_token)
