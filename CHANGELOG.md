# danbot_api Changelog

## 1.0 - 2021-05-31

### Added

- Added examples folder

### Changed

- Uses `discord.ext.tasks` instead of a while loop

### Fixed

- The `NoneType Object has no attribute to '__slots__'` error by utilizing the `discord.ext.tasks` extension

## 0.2 - 2021-05-26

## Added

- Added logging
- Added the `helpers.py` file
- Added a separate class just for http requests
- Added session argument on `DanBotClient`

## Changed

- Using `aiohttp` instead of `requests` as the main HTTP Client/Server
- Made the `key`, and `autopost` arguments on the `DanBotClient` class keyword-only.
