# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Due to specific of json_encoder pagination Page class has been redefined locally in api package. All imports Page, Params and pagination should always imported from api.pagination module  



## [0.0.2] - 2023-07-17

### Added

- Add search for Epeios source API (#REAL-10)
- APM server support with required credentials APM_SERVER_URL, APM_SECRET_TOKEN (#REAL-124).
- Test suite with OAuth2 server browser requirements bypass (#REAL-97)

### Changed

- Flows become dynamic instead of static ()
- Finalized image storage field with required credentials AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET and optional for AWS S3 storage AWS_S3_REGION_NAME (#REAL-97)
