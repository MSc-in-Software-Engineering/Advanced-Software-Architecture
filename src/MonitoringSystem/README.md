Mongodb is setup for the monitoring system by following these steps:

1. Install mongodb
sudo apt install mongodb

2. Start the mongodb service
sudo systemctl start mongodb

3. Enable mongoDB to start on boot
sudo systemctl enable mongodb

4. Verify that MongoDB is running without errors
sudo systemctl status mongodb

5. Interact with MongoDB, using the "mongo" shell
mongo

6. Create a new database
use brickmonitoringdb

7. Create a collection to store data
db.createCollection("brickcount")

8. Setting up mongodb authentication
use admin
db.createUser({
  user: "user",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "brickmonitoringdb" }
  ]
})




