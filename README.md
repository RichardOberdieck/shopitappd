# shopitappd

[![Coverage Status](https://coveralls.io/repos/github/RichardOberdieck/shopitappd/badge.svg?branch=main)](https://coveralls.io/github/RichardOberdieck/shopitappd?branch=main)

This repo integrates [Shopify](https://www.shopify.com/) and [Untappd](https://untappd.com/) for the [Hos Rune](https://hos-rune.dk/) bottleshop.

## Installation
The project uses [hatch](https://hatch.pypa.io/) as a build system, so after creating a virtual env (optional), get started by running `hatch run shopitappd` to execute the scripts, or `hatch run tests` to run the test suite.

## Usage
Currently, the repo covers two things:
1. Add a tag `"4+"` to all products which have a `>= 4` rating on Untappd.
2. Update the rating metafields on Shopify with the ratings from Untappd.

To run the code, execute:

```
hatch run shopitappd
```

The repo is currently set up to run as a cron job using Github Actions. See the corresponding [.yml file](./.github/workflows/schedule.yml) for details.

## How to adapt to your own project
To run this for your own shop, you need three things:
1. A `SHOPIFY_ACCESS_TOKEN`, which you get by registering as a developer in your shopify store.
2. An `UNTAPPD_ACCESS_TOKEN`, which you get from the Untappd for Business part of the website
3. Your `UNTAPPD_SHOP_ID`, which is the last part of the URL for your Untappd presence.

In the code, the access tokens are injected as environment variables in the Github Actions and are stored as secrets. The `UNTAPPD_SHOP_ID` is stored in the [`constants.py](./shopitappd/constants.py).