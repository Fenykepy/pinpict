- / => List of all pins user has access to, most recent up [login required]
    -> redirect to login page if user isn't loggued in
- /login => Modal with login form upon list of all pins, unclosable
- /signup => Modal with register form upon list of all pins, unclosable
- /<user_slug> => List of user's board
- /<user_slug>/pins => List of user's pins
- /<user_slug>/followers => List of user's followers
- /<user_slug>/following => List of users user is following
- /<user_slug>/<board_slug> => List of a board's pins
- /pin/<pin_id> => View specific pin in modal window uppon board's pins list

RESERVED WORDS :
    for usernames :
        login, signup
    for board names :
        pins, followers, following

- Profil page => modal window anywhere
- Add a pin => modal window anywhere
- Add a board => modal window uppon list of boards
- Edit board => modal window uppon board list on pins
