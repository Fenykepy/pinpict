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


redux database (reducers)

user {
}

members {
    'tom': {
        is_fetching: false,
        fetched: true,
        username: 'Tom',
        boards: ['slug', 'slug'],
        pins: ['pk', 'pk'],
        is_fetching_pins: false,
        pins_fetched: false,
        followers: ['slug', 'slug'], // fetched separately
        is_fetching_followers: false,
        followers_fetched: false,
        following: ['slug', 'slug'], // fetched separately
        is_fetching_following: false,
        following_fetched: false,
        ...
    }
}

boards {
    'user_slug_board_slug': {
        is_fetching: false,
        fetched: true,
        pins: ['pk', 'pk']
        ...
    }
}

pins {
    'pk': {
        is_fetching: false,
        fetched: true,
        ...
    }
}

notifications {
    'pk': {
        is_fetching: false,
        fetched: true,
    }
}

