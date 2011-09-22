set :application, "outclan.com"
set :repository,  "git@github.com:vtemian/griddly.git"
set :deploy_to, "/var/www"

set :scm, :git
set :user, "root"  # The server's user for deploys
set :scm_passphrase, "seleus00"  # The deploy user's password
set :branch, "origin/master"
set :git_shallow_clone, 1

role :web, "outclan.com"                          # Your HTTP server, Apache/etc
role :app, "outclan.com"                          # This may be the same as your `Web` server
role :db,  "your primary db-server here", :primary => true # This is where Rails migrations will run
role :db,  "your slave db-server here"
