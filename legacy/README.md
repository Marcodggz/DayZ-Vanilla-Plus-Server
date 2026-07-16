# Legacy server configuration

This directory contains configuration files recovered from a previous version of the **Last Survivor Vanilla+** DayZ server.

Their exact origin and modification status have not yet been verified.

Some or all of these files may contain custom changes. They must be compared against fresh vanilla files downloaded from a newly created Nitrado DayZ PlayStation server before being classified as:

* Vanilla
* Custom
* Active
* Deprecated
* Unused

These files should not be edited directly. Verified configurations will be copied into the appropriate project directories later.

## Private legacy files

The original private Object Spawner files are stored locally under `private/legacy-object-spawners/` and are intentionally excluded from Git.

`krona_0.json` contains the object-spawner configuration of a private base previously used by the server owner and friends.

It includes exact Chernarus coordinates, the complete structure layout and placed equipment. It must not be published directly in the public repository.

A reduced and anonymized example may be created later for documentation and portfolio purposes.

`radio_cenit.json` contains the object-spawner configuration for a custom Black Market area created with a DayZ map editor near Radio Zenit.

The file includes exact coordinates and a large automatically generated collection of structures, props and vegetation. It should be reviewed and reduced before any public release.

A representative and anonymized example may be included later to demonstrate custom map-area design and Object Spawner integration.

`petro.json` contains an unfinished custom oil-facility project planned for the south-east area of Chernarus.

The intended design was a high-value loot zone and PvP hotspot, created entirely as a custom map area. The project was never completed or fully validated on the live server.

It should be classified as an archived prototype rather than an active configuration. Selected fragments may later be used to document the design process, technical experimentation and lessons learned.

## Known modification status

* `globals.xml`: confirmed as modified. `TimeLogin` was set to 5 seconds and `TimeLogout` to 15 seconds. Other possible changes remain unverified.
* `economy.xml`: modification status unknown. It must be compared with a fresh Chernarus vanilla version.

* `events.xml`: confirmed as modified. It contains the custom `VehicleHatchback02_MarcoBlack` event, configured to spawn four black Gunter vehicles with an extended lifetime. The black Gunter entry is commented out in the standard `VehicleHatchback02` event, likely to manage it exclusively through the custom event. Other possible changes remain unverified.

* `cfgeventspawns.xml`: confirmed as modified. It contains four fixed spawn positions for the custom `VehicleHatchback02_MarcoBlack` event defined in `events.xml`. Other possible modifications remain unverified.

* `cfgspawnabletypes.xml`: confirmed as modified. It contains a custom configuration for `Hatchback_02_Black` intended to spawn the four custom vehicles fully assembled and supplied with food, water and medical items. However, the complete block is currently commented out, so it would not be applied by the server. The reason for disabling it is unknown and must be investigated during live testing.

* `types.xml`: confirmed as modified. Multiple ammunition, tool, vehicle-part and survival-item entries use unusually high `nominal` and `min` values, indicating an increased-loot economy. Exact changes must be identified by comparing this file with a fresh vanilla Chernarus version.

* `cfgEffectArea.json`: valid JSON containing the static contaminated areas for Rify and Pavlovo, together with their safe-position coordinates. No custom area has been identified yet. Its modification status remains unverified until it is compared with a fresh vanilla Chernarus file.

* `cfgweather.xml`: contains a complete custom weather configuration, but it is currently disabled through `enable="0"`. Its exact modifications remain unverified until it is compared with a fresh vanilla Chernarus file.

* `messages.xml`: confirmed as modified. It contains bilingual construction warnings shown on player connection and repeated every ten minutes. It also schedules a server shutdown with countdown 109 minutes after startup. This was a temporary development configuration and should not be reused without reviewing the intended restart cycle.


* `zombie_territories.xml`: likely modified. Several military, city and village zones use relatively high dynamic infected ranges, including values up to 20 infected in specific areas. Exact modifications remain unverified until the file is compared with a fresh vanilla Chernarus version.


* `mapgrouppos.xml`: no custom entries have been identified through the initial keyword review. The `Land_Radio_building` result refers to a standard map building rather than the custom Black Market project. Its modification status remains unverified until compared with a fresh vanilla Chernarus file.
