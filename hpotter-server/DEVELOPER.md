# HPotter developer instructions 
These are useful commands for developers

## Git Steps

On your current feature branch:

    git stash 

**Confirm that stash didn't produce an error.** <br>
<br>
Then run:

    git checkout dev

Followed by:

    git pull

After all changes are pulled from the remote, run:

    git checkout "feature branch name"

Now run:

    git rebase dev

Followed by:

    git stash pop

Now run:

    git status

Then:

    git add "all files you want added in to commit"

After this:

    git commit -m "Message about what the commit is for"

Finally:

    git push

## If this is the first push of a branch:

    git push -u origin "feature branch name"
    
## Pull Request reviews

### Pull requests(PR) can be approved by anyone on the team
To pull a branch to perform a PR:

    git branch -t "branch name"

## Network Troubleshooting

When making changes to the network structure, it is important that all previously existing HPotter containers and networks are removed before starting HPotter again.

### Stopping running containers

First, stop all running HPotter containers. If you have no other applications using Docker, this can be done by running:

     docker stop $(docker ps -aq)

If you other applications utilizing docker containers, run:

     docker ps

And then run 'docker stop' followed by the specific containers you wish to stop

### Stopping running networks

Since the network is one of the first parts of HPotter that is spun up, it may be required to manually remove it if there are any errors during shutdown of HPotter

To check if the HPotter network is currently active:

    docker network ls

To remove networks individally (requires no containers attached to the network):

    docker network rm <network name>

To remove containers from a given network:

    docker network disconnect <network name> <container name>

### Removing Docker Volume

Since the average developer will run HPotter multiple times, the docker volume will grow very quickly. "Dangling" containers will stick around and take up a considerable amount of space after a while. So it is important to clear that to avoid some containers from starting and staying up. 
(We had issues on some machines with the MariaDB container staying up)

To check the volume:

    docker volume ls -fq dangling=true

To remove:

    docker volume rm $(docker volume ls -fq dangling=true)

Note: If a developer is running some containers other than HPotter's it is possible for this command to remove more than HPotter's container volumes. 


### MariaDB Not Staying Up 

We suppose MariaDB containers do not stay running after the "mariadb_tls" container is started is due to the fact that we are using the same image for both. This could be particular to the fact that Maria is a database and only one container per a database image can be run a time. 

Solution: Have two different images, one for just "mariadb" and another for "mariadb_tls"

See "Removing Docker Volume" to clear the volume if this and other containers continue to not stay running after startup as well. 


### Authbind (Running HPotter without sudo)

To run HPotter on a dedicated device (i.e. a Raspberry Pi) without administrator privileges, use 'authbind' to facilitate binding sockets of ports 1024 and under like 22, 23, 80, and 443. 

Install Authbind:

""" 
    sudo apt install authbind
"""

Make files in the authbind directory for each port you wish to bind to in HPotter (must use sudo on this step):
"""
    sudo touch /etc/authbind/byport/22
    sudo touch /etc/authbind/byport/23
    sudo touch /etc/authbind/byport/80
    sudo touch /etc/authbind/byport/443
"""

Change the ownership of these files to the user you want to run HPotter with, in this case the user is 'pi' (must use sudo on this step):
"""
    sudo chown pi:pi /etc/authbind/byport/22
    sudo chown pi:pi /etc/authbind/byport/23
    sudo chown pi:pi /etc/authbind/byport/80
    sudo chown pi:pi /etc/authbind/byport/443
"""

Change the permissions of these files to make them executable to the current user (NOTE: sudo is not used on this step):
"""
    chmod 755 /etc/authbind/byport/22
    chmod 755 /etc/authbind/byport/23
    chmod 755 /etc/authbind/byport/80
    chmod 755 /etc/authbind/byport/443
"""

Now HPotter can be run, using the '--depth 3' option specifying how many files down to pass the authbind permssion. In the current version, the ports are bound three files down from running HPotter in "hpotter-server":

"""
    authbind python3 -m hpotter --depth 3 
"""

