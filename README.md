# burner
Burner email

## MANIFEST

Create temporary email addresses for infinte shopping without consequences!


# apach(2) setup

## enable mods

    a2enmod include
    a2enmod cgi

## update config if needed

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/

    <Directory "/usr/lib/cgi-bin">
      Options +ExecCGI
      AddHandler cgi-script .cgi .pl
      Options FollowSymLinks
      Require all granted
    </Directory>

    <Directory /var/www/>
        Options Indexes FollowSymLinks
        Options +Includes
        AddType text/html .shtml
        AddHandler server-parsed .shtml
        AddOutputFilter INCLUDES .shtml
        AllowOverride None
        Require all granted
    </Directory>
