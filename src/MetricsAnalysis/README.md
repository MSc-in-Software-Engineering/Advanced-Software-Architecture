# How to gather plots

Every 10 minutes, plots is being uploaded to a folder within the container. To get the plots to your local machine, run the following command.

Get the running containers, and find the metrics-analysis container id
> docker ps

Copy the folder to your local machine
> docker cp (container id):/plots .
