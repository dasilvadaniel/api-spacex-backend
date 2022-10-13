# SpaceX Satellite Position

The objective of this project is to provide a solution to query the data to determine the last known latitude/longitude of the satellite for a given time, and also finding the closest satellite at a given time T, and a given a position on a globe as a (latitude, longitude) coordinate.

## General Architecture

![api-spacex (2)](https://user-images.githubusercontent.com/27025854/194405263-fa52216d-75e9-4fb0-8c74-3ab1de8b004c.png)

## Folders

    ├── reports                		 # Lambda functions to perform SQL queries on the database
    │   ├── satellite_closest
	│   │   └── lambda_function.py
    │   ├── satellite_position
	│   │   └── lambda_function.py
    ├── src               			 # Container code read raw data from S3 and send it to RDS
    │   ├── mains.py	
	│   └── requirements.txt
    ├── Dockerfile
    └── README.md

## Getting started

To use this API you just need to send a POST request (using Postman) to the following URL with the respective body.

### Last satellite location 
Request to get the last known latitude/longitude of the satellite for a given time:

Endpoit:
https://test-endpoint.execute-api.us-east-2.amazonaws.com/starlink/satelliteposition

Body:
``` 
{
  "date": "2021-01-26",
  "satellite_id": "5eed7714096e5900069856cb"
}
```

Response:
```
{
    "id": "5eed7714096e5900069856cb",
    "longitude": 0,
    "latitude": -51.329096537437835
}
```

### Closest Satellite
API to find the closest satellite at a given time T, and a given a position on a globe as a (latitude, longitude) coordinate.

Endpoit:
https://test-endpoint.execute-api.us-east-2.amazonaws.com/starlink/satelliteclosest

Body:
```
{
  "date": "2021-01-26",
  "latitude": "0",
  "longitude": "0"
}
```

Response:
```
{
    "id": "60106f1fe900d60006e32c82",
    "longitude": 1,
    "latitude": -0.6063283889091351,
    "distance": 80.80630190802876
}
```

## Running the container locally

### Requirements

[Docker](https://docs.docker.com/)

[AWS Client](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

After the installations you need to create an IAM user and [configure the credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html):

```
$ aws configure
AWS Access Key ID [None]: 
AWS Secret Access Key [None]: 
Default region name [None]: 
Default output format [None]:
```

You also need to attach the following read/write permissions to the user:

```
S3
Secrets Manager
RDS
```

After that, you need to store the raw data in a S3 bucket and create an empty Postgres database on RDS.

Finally, store the following variables on a `starlink-credentials` secret on Secrets Manager:

```
rds_user	database_user
rds_password	database_password
rds_endpoint	{database_name}.{aws-account}.{aws-region}.rds.amazonaws.com
rds_port	database_port
rds_database	starlink
s3_raw_data	s3://{bucket}/
rds_full_result	starlink_historical_data
```

### Running the docker container

The docker container to run on ECS is available at [DockerHub](https://hub.docker.com/repository/docker/dasilvadanielantonio/blueonion-startlink-api).

You can also clone this repository and run the following commands:

```
cd api-spacex-backend
docker build -t blueonion-startlink-api . 
docker run blueonion-startlink-api 
```

## Authors

* **Daniel Antonio da Silva** - [GitHub](https://github.com/dasilvadaniel)
