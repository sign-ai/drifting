# Server architecture

Drift Detection Server is made of 2 mandatory components and one optional
component.

Mandatory components are `Server` and `Artifacts Storage`. Obligatory component
is `Metrics Database`.

## Server

Server is a Python FastAPI server.

## Artifacts Storage

Artifacts Storage is a storage where Projects are stored. Additionally, it
has a store.json file, that keeps the information about all the available
models and their status.
The storage follows a simple directory structure:

```nohighlight
└── drifting/
    ├── store.db                   <- key-value store with model paths
    ├── active.db                  <- key-value store with model statuses
    ├── project1/
    │   |── configuration.yaml     <- Drift Detector configuration
    │   └── drift_detector.joblib  <- Drift Detector parameters
    └── project2/
        |── configuration.yaml     <- Drift Detector configuration
        └── drift_detector.joblib  <- Drift Detector parameters
```

Artifacts Storage can be a local directory, or external storage service.

## Metrics Database

Metrics Database is a Postgres database that stores the metrics for a given
Project.

Database schemas allow to store the drift value for each request over time.
Therefore it can be used to illustrate the drift trend over time for each
Project.

However, `drifting` package is not focused on metrics storage nor presentation.
This has 2 reasons:

- Drift metrics are returned after each `/predict` request. Therefore it's easy
  for a user to manage on client side.
- Every organization uses different logging and tracking tools, and databases.
  We believe it is the best to leave the metrics storing, presenting and
  decision-making to the client.

# Deployment scenarios

Drift Detection Server can be run in three modes:

1. Simple deployment - a simple deployment, advised to be run locally on
   in the development environment, and for simple production use-cases.

2. Cloud Native deployment - this is a setup that follows the Cloud Native
   manifests

## 1: Simple deployment

After running:

`drifting serve`

a simple deployment is ready.

Local directory `artifact_path` is created for storing artifacts (Projects). The
default path is `.drifiting/`.

Local Postgres database is created for managing. Optionally database creation
can be turned off.

After Drift Detector is fitted, it is stored in `artifact_path`. If any other
artifacts exists in the `artifact_path`, they are loaded according to
configuration.

### Simple deployment for a production use-case

This can be used on remote instance. For example on EC2. It's not
Cloud-Native-level deployment, but may be simple and useful for for many cases,
especially at the beginning of the project, where all the advantages are not
obvious yet.

If the instance can be reached externally, it's ready to be used. After the
users will decide there's a need for Cloud Native deployment, it's easy to
copy the `artifact_path` to external storage service, like S3 or Google Cloud
Storage.

## 2: Cloud Native deployment

Another way of deployment is to deploy artifacts storage, database, and
Drift Detection Server separately.

`drifting serve --artifacts_path=s3://bucketname/drifting --database_uri postgres:///drifting.db`

Artifacts path is Amazon S3 or Google Cloud Storage. The server has to have
permissions to save artifacts on the external storage. See
`Configuring access to external storage`.

Note, that the database is used only for storing the metrics, is optional,
and doesn't impact any regular functionality of the server.
If `database_uri` is not set, no database is created and the metrics are not
saved. They can still be managed on client's side.

### Configuring access to external storage

Currently only Amazon S3 or Google Cloud Storage are supported.

#### Google Cloud Storage

Use service account TODO

#### Amazon S3

Any authentication on the server TODO.
