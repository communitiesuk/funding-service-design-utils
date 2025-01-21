### 6.0.2

* Allowing for the `Config` module to live in either `config` or `pre_award.config`.

[This RFC](https://github.com/communitiesuk/funding-service-requests-for-comments/discussions/22) outlines the move of all the existing code into a top level `pre_award` folder while we consolidate an simplify the code. We need to continue to support both paths though as FAB also uses this fixture, but does not have a `pre_award` folder.

### 6.0.1

* Revert: "Fix a DeprecationWarning from pythonjsonlogger" which actually broke things
* Revert: "Removes `locale_selector` module, which has now been lifted directly into `pre-award-frontend` (and modified to support `host_matching` mode)." because this is still used by pre-award-stores

### 6.0.0

* Removes `locale_selector` module, which has now been lifted directly into `pre-award-frontend` (and modified to support `host_matching` mode).

### 5.3.1

* Fix a DeprecationWarning from pythonjsonlogger

### 5.3.0

* Update the Healthcheck to support apps running in `host_matching` mode.

### 5.2.0

* Adding check internal user functionality and adding FAB and Form Designer to list of supported apps

### 5.1.10

* Running `uv lock` when version incremented

### 5.1.9

* Changing to a negative check for the environment list

### 5.1.8

* Overriding the central rangeStrategy=pin

### 5.1.7

* No functional changes (fix packaging with uv).

### 5.1.6

* No functional changes (switch over to using uv).

### 5.1.5

* No functional changes (bumping local pre-commit).

### 5.1.4
* Revert 5.3.1, as forcing secure=true is broken for local development in some cases (where HTTPS is not used). To be fixed properly by another future patch.

### 5.1.3

* Make the `lang` cookie secure/httponly/samesite=lax.

### 5.1.2

- Return default language as "en" if "language" cookie is not " en/cy "

### 5.1.1

- BAU: Update redirect

### 5.1.0

- Make Table config print optional; set FSD_UTILS_ENABLE_CONFIG_TABLE in the
env to decide

### 5.0.6

- Un-pinned various dependencies

### 5.0.5

- add boto3 dependency to fsd-utils; wasn't included correctly before

### 5.0.4

- add some GOV.UK Notify constants for pre-award

### 5.0.3

- remove some upper-bound pins on dependencies

### 5.0.2

- no external changes

### 5.0.1

- `login_required` now always checks for a valid session cookie before falling back to a DEBUG_USER in development environments.

# 5.0.0 (breaking change)

- `fsd_utils.toggles` has been made an optional extra, so its dependencies are not installed automatically. If your
  uses the `toggles` module, then you should change your `requirements.txt` from `funding-service-design-utils` to
  `funding-service-design-utils[toggles]`.
