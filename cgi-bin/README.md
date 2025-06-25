# cgi commands

The cgi script (erlang) controls access to the file burner.config

    /var/www/data/burner.config            # linux
    /Library/WebServer/data/burner.config  # mac os

There are commands to add/delete and modify the config data. The
commands also remotly update the mail server through mail server scripts
when needed.

## Query string

The burner-action.cgi script read the command query from
the first arguments or the environment variable "QUERY_STRING". The query string
is required to be on a url query format

   key1=value1&key2=value2...

A key only field is the same as key=true


## Burner actions

The key action is mandatory and determin the actions. The following
action commands are implemented:

    add	     Add a new alias to the config

    del	     Delete an alias entry

    mod	     Modify an alias entry

    set	     Set global configuration items

    list     Debug command to list the config to standard output

## Actions

### action=list

List the output to the standard output, for refresh or debug if no
other action is requested.

### action=add&alias=joe[&items]

Add a new alias (joe) entry to the config, or fail if already present.
The available keys that can be set are:

    block, site, password, comment

### action=del&alias=joe

Remove an entry from the config file if present, or fail if not.


### action=mod&alias=joe[&items]

Modify an existing alias (joe) entry, or fail if not present.
The available keys that can be modified are:

    block, site, password, comment

### action=set&key=KEY&value=VALUE

Create or update a global config item, for example
the mail "domain" name, main "username" etc.
This item is open to store various key value paris.

## config items

    block=boolean()

	Block/Unblock the alias. The alias is temporarily removed if block=true
	or re-added when block=false

    site=string()

	The (optional) site where the email-alias where added for,
	like a shopping site or similar.

    password=string()

	The (optional) password used on the vendor site when the email alias
	where created.

    comment=string()

	An (optional) descriptive text that can be anythimg you like.
