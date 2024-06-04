# Dashboard, protected by OAuth2/JWT


### "anonymous can access index route"
    (As an `Anonymous`, I want to `access the index route`, so I can _see unprivileged content_)

    Given: An anonymous visitor
    When: The index route accessed
    Then: Unprivileged content is available

### "anonymous can log in"
    (As an `Anonymous`, I want to `log in with my OAuth2 credentials`, so I can _become an authenticated user_)

    Given: An anonymous visitor
    When: The login route is accessed
    Then: The visitor is redirected to OAuth2 provider to begin authentication flow

### "user identity stored client-side"
    (As a `Programmer`, I want to `store the user's identity client-side via secure jwt cookie`, so I can _determine which user is authenticated_)

    Given: A user returning from a completed OAuth2 flow
    When: The system is supplied with the oauth2 id
    Then: A JWT cookie containing the oauth2 id is generated and stored client-side

### "user credentials stored server-side"
    (As a `Programmer`, I want to `store the user's access and refresh tokens server-side `, so I can _securely act on behalf of the authenticated user_)

    Given: A user returning from a completed OAuth2 flow
    When: The system is supplied with the oauth2 id, access and refresh tokens
    Then: The oauth2 id, access and refresh tokens are stored server-side

### "users are redirected after login"
    (As an `User`, I want to `be returned to where I began the login process after successful authentication`, so _I can resume my activities without additional steps_)

    Given: A visitor begins OAuth2 flow from a particular route
    When: The visitor completes flow as a user
    Then: The user is returned to that particular route 

### "user credentials are remembered"
    (As a `User`, I want to `have my OAuth2 credentials remembered`, so I can _access priviledged resources until my session ends_)
    (As a `User`, I want to `make calls to the provider's API using my credentials`, so I can _explore the data returned_)

    Given: A user session containing user's oauth2 id
    When: Accessing the OAuth2 provider's API
    Then: The system uses the user's stored credentials

### "access tokens are refreshed as needed"
    (As a `Programmer`, I want to `refresh a user's access token when needed`, so I can _reduce the number of user authentications required_)

    Given: A user accesses the system
    When: The stored access token requires refreshing
    Then: The system obtains refreshed tokens
    And: The system updates the stored credentials

### "expired access token requires re-authentication"
    (As a `Programmer`, I want to `end a user's session if credentials become invalid`, so I can _force the user to re-authenticate to maintain security_)

    Given: A user with an active session and non-refreshable expired credentials
    When: The system fails to refresh the credentials
    Then: The system destroys the session

### "user can log out"
    (As a `User`, I want to `log out`, so I can _end my session securely_)

    Given: A user with an active session
    When: The user accesses the log out route
    Then: The session is destroyed
    And: The user is redirected to the index route

### "dashboard allows authenticated users"
    (As a `User`, I want to `access the Dashboard`, so I can _use the privileged tools provided_)

    Given: A user session containing a user's oauth2 id
    When: The Dashboard route is accessed
    Then: Privileged content is available

### "dashboard redirects anonymous visitors to login"
    (As an `Admin`, I want to `protect the Dashboard route`, so _only authenticated Users may access it_)
    (As an `Admin`, I want to `redirect anonymous visitors from protected routes to the login route`, so _the user may authenticate_)

    Given: An anonymous visitor
    When: The Dashboard route is accessed
    Then: The visitor is redirected to the login route

### "system provides navigation links"
    (As a `User`, I want to `navigate easily using links`, so I _don't have to type in addresses manually_)

    Given: A visitor
    When: Index route is accessed
    Then: Visitor sees links to 'index' and 'log in' routes

    Given A user
    When: Index or Dashboard routes are accessed
    Then: User sees links to 'index', 'dashboard' and 'log out'
