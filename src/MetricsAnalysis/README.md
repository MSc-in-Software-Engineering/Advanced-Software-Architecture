# MetricsAnalysis

Every 10 minutes, line and box plots is being uploaded to a folder called _plots_ within the container. To get the plots to your local machine, run the followings command.

Be aware the architecture needs to be running to ensure metrics analysis is running correctly, as this service was made specifically to accomodate an performance experiment.

1. Request a list of the running containers, and find the id for the metrics-analysis container:

> docker ps

2. Copy the _plots_ folder to your local machine

> docker cp (container id):/plots .

3. You are now able to investigate the performance of the architecture conducted.

No interaction needed, it starts by itself.
