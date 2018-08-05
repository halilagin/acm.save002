#!/bin/bash
echo "you are about to delete all images permanently, are you sure (print yes):"

read answer

if [ "$answer" == "yes" ]; then
	# Delete all containers
	docker rm $(docker ps -a -q)
	# Delete all images
	docker rmi $(docker images -q)
	exit
fi

echo "cancelling..."
exit

