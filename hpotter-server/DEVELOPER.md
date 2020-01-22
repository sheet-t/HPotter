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
