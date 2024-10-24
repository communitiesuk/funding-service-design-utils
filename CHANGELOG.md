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
