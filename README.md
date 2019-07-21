Yang-site health
=======

## Service that exersizes URLs on YangCatalog site to look for errors. 

Uses an internal copy of postman config file for list of URLs to exersize.

### URL SCHEME

* /  =>   the home page
* /run => list of the the test runs       
* /run/{run_id}/ => details about a particular run
* /run-new POST => run a new test
* /errors => last 20 errors
* /endpoint => list of all tests
* /endpoint/{endpoint_id} => history about a particular test
