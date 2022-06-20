# funding-service-design-utils
Shared library for funding service design apps. 

This library can be installed into other python repos and the packages used by those repos.

# Releasing
To create a new release of funding-service-design-utils:
1. Make and test your changes as normal in this repo
2. Update the `version` tag in `setup.py`
3. Push your changes to `main`.
4. The Action at `.github/workflows/create-tag-workflow.yml` will create a new tag and release, named for the version in `setup.py`. This is triggered automatically on a push to main.

# Usage
Either of the following options will install the funding-service-design-utils into your python project. The package `fsd_utils` can then be imported.
## Tagged version
To reference a particular tag from pip, add the following to your `requirements.txt` file or use `pip install`:
    
    hhttps://github.com/communitiesuk/funding-service-design-utils/archive/refs/tags/<tagName>.tar.gz

## Latest / in-dev version
To reference the latest commit from a particular branch from pip, add the following to your `requirements.txt` file or use `pip install`:
    
    git+https://github.com/communitiesuk/funding-service-design-utils.git@<branchName>