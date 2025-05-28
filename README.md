# burner
Burner email

## MANIFEST

Create temporary email addresses for infinte shopping without consequences!

# mac os setup

## enable mods

## update /etc/apache2/httpd.conf

Enable cgi and include mods by uncomment mod_include and mod_cgi

    Load mod_include.so
    Load mod_cgi.so

## Put burner_action.cgi in cgi directory

    sudo cp cgi-bin/burner_action.cgi /Library/WebServer/CGI-Excutable/
    sudo chown root:wheel /Library/WebServer/CGI-Excutable/burner_action.cgi

# apache(2) setup

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
