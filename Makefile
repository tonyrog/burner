#
# Some simple install commands
#

install_linux_www:
	sudo cp -f cgi-bin/burner_action.cgi /usr/lib/cgi-bin/
	sudo cp -rf www/html/* /var/www/html/
#
# Install a new fresh demo burner.config
#
install_linux_data:
	sudo mkdir -p /var/www/data
	chown www-data:www-data /var/www/data
	sudo cp -f data/burner.config /var/www/data/
	chown www-data:www-data /var/www/data/burner.config


install_macos_www:
	sudo cp -f cgi-bin/burner_action.cgi /Library/WebServer/CGI-Excutable/
	sudo chown root:wheel /Library/WebServer/CGI-Excutable/burner_action.cgi
	sudo cp -rf www/html/* /Library/WebServer/Document/
#
# Install a new fresh demo burner.config
#
install_macos_data:
	sudo mkdir -p /Library/WebServer/data
	chown _www:_www /Library/WebServer/data
	sudo cp -f data/burner.config /Library/WebServer/data/
	chown _www:_www /Library/WebServer/data/burner.config
