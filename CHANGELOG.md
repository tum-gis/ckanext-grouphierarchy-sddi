# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
For releases `< 1.0.0` minor version steps may indicate breaking changes too.

## [1.1.3] - 2023-10-13
### Added
Reducing the number of emails sent for the "Forgot your password?" function
### Fixed
Cross-Site-Scripting problems mentioned [here](https://github.com/tum-gis/ckan-docker/pull/40)

## [1.1.2] - 2023-07-05
### Fixed
- small bugfixes (see [#17](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/issues/17))
-  Extended licenses list required for SDDI is added (see [here](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/blob/main/ckanext/grouphierarchy/licenses_SDDI.json) )

## [1.1.1] - 2023-07-05
### Fixed
Small bugfixes

### Added
Update of the Organization list (`init_data.json` file) and their logos.

## [1.1.0] - 2023-06-27

### Changed
Personalization of SDDI CKAN via config variables mentioned [here](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/issues/8)

## [1.0.1] - 2023-04-28

### Fixed
Bugfixes [#7](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/pull/7)

### Added
- German translation
- Funcionality from [ckanext-userautoaddgroup-sddi](https://github.com/tum-gis/ckanext-userautoaddgroup-sddi) is added to the extension. When user is registered, he will be automaticaly assigned to the main categories and topics, which allows them to create datasets for this category or topic.

## [1.0.0] - 2023-04-28

### Changed
Compatibility with ckan > v2.9.0

## [ckan-2.8] - 2023-03-16

This Release of the CKAN extension is intended to be used in combination with the [SDDI CKAN Docker container](https://github.com/tum-gis/SDDI-CKAN-Docker) and is tested just only with CKAN 2.8.0

## [template] - YYYY-MM-DD

### Added

### Changed

### Removed

### Fixed

### Security

### Deprecated

### Known issues

## [template] - YYYY-MM-DD

### Added

### Changed

### Removed

### Fixed

### Security

### Deprecated

### Known issues

[Unreleased]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/compare/0.0.5...HEAD
[1.1.3]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/compare/1.1.2...1.1.3
[1.1.2]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/compare/ckan-2.8...1.0.0
[ckan-2.8]: https://github.com/tum-gis/ckanext-grouphierarchy-sddi/releases/ckan-2.8
[template]: https://keepachangelog.com/en/1.0.0/
