# Advanced Software Architecture

## About

- Group: **_Group 1_**
- Domain: **_Industry 4.0 production_**
- Product: **_Recycling of used Lego bricks_**
- System: **_Cyber-physical system_**
- Supply chain: **_Collect used Lego bricks, sort accordingly for recyclable usage, and distribute in packages to customers._**

## Source code and CI/CD workflow

Code for each of the services within the infrastructure are in the folder **_src_**.

Additionally two compose files has been created, one utilized for the CI/CD workflow **_(docker-compose.prod.yml)_** and one for local usage **(docker-compose.yml)**.

To run the CI/CD workflow from commit to deployment and release, ensure that the self-runner for the deployment step is running on the local machine. Beware that you might need to authorize [GitHub container registry](https://www.andrewhoog.com/post/authorizing-github-container-registry/).

The VM utilized for this repository in which deployment is being made is on the machine **_bds-g01-n1_**.

At last, ensure that a VPN connection to SDU's network is established.

## Provided subsystems

Navigation to each of the subsystems that are part of the overall architecture.

- [Warehouse](src/Warehouse/)
- [WarehouseSystem](src/WarehouseSystem/)
- [Customer Service Subsystem](src/CustomerService/)
- [MQTT Mediator](src/MQTTMediator/)
- [MQTT Warehouse](src/MQTTWarehouse/)
- [Productions floor: Robotics](src/ProductionFloor/Robotics/)
- [Productions floor: IoT](src/ProductionFloor/IoT/)
- [Productions floor: ConveyorBelts](src/ProductionFloor/ConveyorBelts/)
- [Monitoring Subsystem](src/MonitoringSystem/)
- [Metrics Analysis](src/MetricsAnalysis/)
- [SupplyChainManagementDatabase](srcSupplyChainManagementDatabase/)
