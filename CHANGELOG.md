# 5.0.0 (breaking change)

- `fsd_utils.toggles` has been made an optional extra, so its dependencies are not installed automatically. If your
  uses the `toggles` module, then you should change your `requirements.txt` from `funding-service-design-utils` to
  `funding-service-design-utils[toggles]`.
