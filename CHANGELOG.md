# Docker Community Collection Release Notes

**Topics**

- <a href="#v2-7-13">v2\.7\.13</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v2-7-12">v2\.7\.12</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v2-7-11">v2\.7\.11</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v2-7-10">v2\.7\.10</a>
    - <a href="#release-summary-3">Release Summary</a>
    - <a href="#bugfixes-3">Bugfixes</a>
    - <a href="#known-issues">Known Issues</a>
- <a href="#v2-7-9">v2\.7\.9</a>
    - <a href="#release-summary-4">Release Summary</a>
    - <a href="#security-fixes">Security Fixes</a>
- <a href="#v2-7-8">v2\.7\.8</a>
    - <a href="#release-summary-5">Release Summary</a>
    - <a href="#bugfixes-4">Bugfixes</a>
- <a href="#v2-7-7">v2\.7\.7</a>
    - <a href="#release-summary-6">Release Summary</a>
    - <a href="#bugfixes-5">Bugfixes</a>
- <a href="#v2-7-6">v2\.7\.6</a>
    - <a href="#release-summary-7">Release Summary</a>
    - <a href="#bugfixes-6">Bugfixes</a>
- <a href="#v2-7-5">v2\.7\.5</a>
    - <a href="#release-summary-8">Release Summary</a>
    - <a href="#bugfixes-7">Bugfixes</a>
- <a href="#v2-7-4">v2\.7\.4</a>
    - <a href="#release-summary-9">Release Summary</a>
    - <a href="#bugfixes-8">Bugfixes</a>
- <a href="#v2-7-3">v2\.7\.3</a>
    - <a href="#release-summary-10">Release Summary</a>
    - <a href="#bugfixes-9">Bugfixes</a>
- <a href="#v2-7-2">v2\.7\.2</a>
    - <a href="#release-summary-11">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v2-7-1">v2\.7\.1</a>
    - <a href="#release-summary-12">Release Summary</a>
    - <a href="#bugfixes-10">Bugfixes</a>
- <a href="#v2-7-0">v2\.7\.0</a>
    - <a href="#release-summary-13">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#deprecated-features">Deprecated Features</a>
    - <a href="#bugfixes-11">Bugfixes</a>
- <a href="#v2-6-0">v2\.6\.0</a>
    - <a href="#release-summary-14">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#deprecated-features-1">Deprecated Features</a>
    - <a href="#bugfixes-12">Bugfixes</a>
- <a href="#v2-5-1">v2\.5\.1</a>
    - <a href="#release-summary-15">Release Summary</a>
    - <a href="#bugfixes-13">Bugfixes</a>
- <a href="#v2-5-0">v2\.5\.0</a>
    - <a href="#release-summary-16">Release Summary</a>
    - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v2-4-0">v2\.4\.0</a>
    - <a href="#release-summary-17">Release Summary</a>
    - <a href="#minor-changes-4">Minor Changes</a>
    - <a href="#bugfixes-14">Bugfixes</a>
- <a href="#v2-3-0">v2\.3\.0</a>
    - <a href="#release-summary-18">Release Summary</a>
    - <a href="#minor-changes-5">Minor Changes</a>
    - <a href="#bugfixes-15">Bugfixes</a>
- <a href="#v2-2-1">v2\.2\.1</a>
    - <a href="#release-summary-19">Release Summary</a>
    - <a href="#bugfixes-16">Bugfixes</a>
- <a href="#v2-2-0">v2\.2\.0</a>
    - <a href="#release-summary-20">Release Summary</a>
    - <a href="#minor-changes-6">Minor Changes</a>
    - <a href="#bugfixes-17">Bugfixes</a>
- <a href="#v2-1-1">v2\.1\.1</a>
    - <a href="#release-summary-21">Release Summary</a>
    - <a href="#bugfixes-18">Bugfixes</a>
- <a href="#v2-1-0">v2\.1\.0</a>
    - <a href="#release-summary-22">Release Summary</a>
    - <a href="#minor-changes-7">Minor Changes</a>
    - <a href="#bugfixes-19">Bugfixes</a>
- <a href="#v2-0-2">v2\.0\.2</a>
    - <a href="#release-summary-23">Release Summary</a>
    - <a href="#bugfixes-20">Bugfixes</a>
- <a href="#v2-0-1">v2\.0\.1</a>
    - <a href="#release-summary-24">Release Summary</a>
- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#release-summary-25">Release Summary</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
    - <a href="#deprecated-features-2">Deprecated Features</a>
    - <a href="#removed-features-previously-deprecated">Removed Features \(previously deprecated\)</a>
- <a href="#v1-10-0">v1\.10\.0</a>
    - <a href="#release-summary-26">Release Summary</a>
    - <a href="#minor-changes-8">Minor Changes</a>
- <a href="#v1-9-1">v1\.9\.1</a>
    - <a href="#release-summary-27">Release Summary</a>
    - <a href="#bugfixes-21">Bugfixes</a>
- <a href="#v1-9-0">v1\.9\.0</a>
    - <a href="#release-summary-28">Release Summary</a>
    - <a href="#minor-changes-9">Minor Changes</a>
    - <a href="#deprecated-features-3">Deprecated Features</a>
    - <a href="#bugfixes-22">Bugfixes</a>
    - <a href="#new-plugins">New Plugins</a>
        - <a href="#connection">Connection</a>
- <a href="#v1-8-0">v1\.8\.0</a>
    - <a href="#release-summary-29">Release Summary</a>
    - <a href="#minor-changes-10">Minor Changes</a>
    - <a href="#bugfixes-23">Bugfixes</a>
- <a href="#v1-7-0">v1\.7\.0</a>
    - <a href="#release-summary-30">Release Summary</a>
    - <a href="#minor-changes-11">Minor Changes</a>
- <a href="#v1-6-1">v1\.6\.1</a>
    - <a href="#release-summary-31">Release Summary</a>
    - <a href="#bugfixes-24">Bugfixes</a>
- <a href="#v1-6-0">v1\.6\.0</a>
    - <a href="#release-summary-32">Release Summary</a>
    - <a href="#minor-changes-12">Minor Changes</a>
    - <a href="#deprecated-features-4">Deprecated Features</a>
    - <a href="#bugfixes-25">Bugfixes</a>
- <a href="#v1-5-0">v1\.5\.0</a>
    - <a href="#release-summary-33">Release Summary</a>
    - <a href="#minor-changes-13">Minor Changes</a>
    - <a href="#bugfixes-26">Bugfixes</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v1-4-0">v1\.4\.0</a>
    - <a href="#release-summary-34">Release Summary</a>
    - <a href="#minor-changes-14">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide-1">Breaking Changes / Porting Guide</a>
    - <a href="#security-fixes-1">Security Fixes</a>
    - <a href="#bugfixes-27">Bugfixes</a>
- <a href="#v1-3-0">v1\.3\.0</a>
    - <a href="#release-summary-35">Release Summary</a>
    - <a href="#minor-changes-15">Minor Changes</a>
    - <a href="#bugfixes-28">Bugfixes</a>
    - <a href="#new-modules-1">New Modules</a>
- <a href="#v1-2-2">v1\.2\.2</a>
    - <a href="#release-summary-36">Release Summary</a>
    - <a href="#security-fixes-2">Security Fixes</a>
- <a href="#v1-2-1">v1\.2\.1</a>
    - <a href="#release-summary-37">Release Summary</a>
    - <a href="#bugfixes-29">Bugfixes</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#release-summary-38">Release Summary</a>
    - <a href="#minor-changes-16">Minor Changes</a>
    - <a href="#bugfixes-30">Bugfixes</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#release-summary-39">Release Summary</a>
    - <a href="#minor-changes-17">Minor Changes</a>
    - <a href="#deprecated-features-5">Deprecated Features</a>
    - <a href="#bugfixes-31">Bugfixes</a>
    - <a href="#new-plugins-1">New Plugins</a>
        - <a href="#connection-1">Connection</a>
        - <a href="#inventory">Inventory</a>
    - <a href="#new-modules-2">New Modules</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#release-summary-40">Release Summary</a>
    - <a href="#bugfixes-32">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary-41">Release Summary</a>
    - <a href="#minor-changes-18">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#release-summary-42">Release Summary</a>
    - <a href="#minor-changes-19">Minor Changes</a>
    - <a href="#removed-features-previously-deprecated-1">Removed Features \(previously deprecated\)</a>
    - <a href="#bugfixes-33">Bugfixes</a>

<a id="v2-7-13"></a>
## v2\.7\.13

<a id="release-summary"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes"></a>
### Bugfixes

* docker\_prune \- fix handling of lists for the filter options \([https\://github\.com/ansible\-collections/community\.docker/issues/961](https\://github\.com/ansible\-collections/community\.docker/issues/961)\, [https\://github\.com/ansible\-collections/community\.docker/pull/966](https\://github\.com/ansible\-collections/community\.docker/pull/966)\)\.

<a id="v2-7-12"></a>
## v2\.7\.12

<a id="release-summary-1"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-1"></a>
### Bugfixes

* docker\_container \- fix possible infinite loop if <code>removal\_wait\_timeout</code> is set \([https\://github\.com/ansible\-collections/community\.docker/pull/922](https\://github\.com/ansible\-collections/community\.docker/pull/922)\)\.

<a id="v2-7-11"></a>
## v2\.7\.11

<a id="release-summary-2"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-2"></a>
### Bugfixes

* docker\_compose \- make sure that the module uses the <code>api\_version</code> parameter \([https\://github\.com/ansible\-collections/community\.docker/pull/881](https\://github\.com/ansible\-collections/community\.docker/pull/881)\)\.

<a id="v2-7-10"></a>
## v2\.7\.10

<a id="release-summary-3"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-3"></a>
### Bugfixes

* EE requirements \- restrict <code>requests</code> dependency to <code>\< 2\.32\.0</code> since later versions are incompatible with Docker SDK for Python \< 7\.1\.0\, which we depend on \([https\://github\.com/ansible\-collections/community\.docker/pull/872](https\://github\.com/ansible\-collections/community\.docker/pull/872)\)\.

<a id="known-issues"></a>
### Known Issues

* EE requirements \- <code>requests \< 2\.32\.0</code> is vulnerable to [CVE\-2024\-35195](https\://github\.com/advisories/GHSA\-9wx4\-h78v\-vm56)\. This does not affect Docker SDK for Python\, but might affect other users of <code>requests</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/872](https\://github\.com/ansible\-collections/community\.docker/pull/872)\)\.

<a id="v2-7-9"></a>
## v2\.7\.9

<a id="release-summary-4"></a>
### Release Summary

Bugfix release\.

<a id="security-fixes"></a>
### Security Fixes

* docker\_containers\, docker\_machine\, and docker\_swarm inventory plugins \- make sure all data received from the Docker daemon / Docker machine is marked as unsafe\, so remote code execution by obtaining texts that can be evaluated as templates is not possible \([https\://www\.die\-welt\.net/2024/03/remote\-code\-execution\-in\-ansible\-dynamic\-inventory\-plugins/](https\://www\.die\-welt\.net/2024/03/remote\-code\-execution\-in\-ansible\-dynamic\-inventory\-plugins/)\, [https\://github\.com/ansible\-collections/community\.docker/pull/815](https\://github\.com/ansible\-collections/community\.docker/pull/815)\)\.

<a id="v2-7-8"></a>
## v2\.7\.8

<a id="release-summary-5"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-4"></a>
### Bugfixes

* Execution Environment requirements \- restrict Docker SDK for Python to \< 7\.0\.0\, as 7\.0\.0 is incompatible with docker\-compose \([https\://github\.com/ansible\-collections/community\.docker/pull/719](https\://github\.com/ansible\-collections/community\.docker/pull/719)\)\.
* modules and plugins using the Docker SDK for Python \- remove <code>ssl\_version</code> from the parameters passed to Docker SDK for Python 7\.0\.0\+\. Explicitly fail with a nicer error message if it was explicitly set in this case \([https\://github\.com/ansible\-collections/community\.docker/pull/715](https\://github\.com/ansible\-collections/community\.docker/pull/715)\)\.
* modules and plugins using the Docker SDK for Python \- remove <code>tls\_hostname</code> from the parameters passed to Docker SDK for Python 7\.0\.0\+\. Explicitly fail with a nicer error message if it was explicitly set in this case \([https\://github\.com/ansible\-collections/community\.docker/pull/721](https\://github\.com/ansible\-collections/community\.docker/pull/721)\)\.

<a id="v2-7-7"></a>
## v2\.7\.7

<a id="release-summary-6"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-5"></a>
### Bugfixes

* docker\_swarm \- make init and join operations work again with Docker SDK for Python before 4\.0\.0 \([https\://github\.com/ansible\-collections/community\.docker/issues/695](https\://github\.com/ansible\-collections/community\.docker/issues/695)\, [https\://github\.com/ansible\-collections/community\.docker/pull/696](https\://github\.com/ansible\-collections/community\.docker/pull/696)\)\.
* docker\_volume \- fix crash caused by accessing an empty dictionary\. The <code>has\_different\_config\(\)</code> was raising an <code>AttributeError</code> because the <code>self\.existing\_volume\[\"Labels\"\]</code> dictionary was <code>None</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/702](https\://github\.com/ansible\-collections/community\.docker/pull/702)\)\.

<a id="v2-7-6"></a>
## v2\.7\.6

<a id="release-summary-7"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-6"></a>
### Bugfixes

* docker\_swarm\_info \- if <code>service\=true</code> is used\, do not crash when a service without an endpoint spec is encountered \([https\://github\.com/ansible\-collections/community\.docker/issues/636](https\://github\.com/ansible\-collections/community\.docker/issues/636)\, [https\://github\.com/ansible\-collections/community\.docker/pull/637](https\://github\.com/ansible\-collections/community\.docker/pull/637)\)\.

<a id="v2-7-5"></a>
## v2\.7\.5

<a id="release-summary-8"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-7"></a>
### Bugfixes

* docker\_prune \- return correct value for <code>changed</code>\. So far the module always claimed that nothing changed \([https\://github\.com/ansible\-collections/community\.docker/pull/593](https\://github\.com/ansible\-collections/community\.docker/pull/593)\)\.
* various plugins and modules \- remove unnecessary imports \([https\://github\.com/ansible\-collections/community\.docker/pull/574](https\://github\.com/ansible\-collections/community\.docker/pull/574)\)\.

<a id="v2-7-4"></a>
## v2\.7\.4

<a id="release-summary-9"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-8"></a>
### Bugfixes

* docker\_api connection plugin \- fix error handling when 409 Conflict is returned by the Docker daemon in case of a stopped container \([https\://github\.com/ansible\-collections/community\.docker/pull/546](https\://github\.com/ansible\-collections/community\.docker/pull/546)\)\.
* docker\_container\_exec \- fix error handling when 409 Conflict is returned by the Docker daemon in case of a stopped container \([https\://github\.com/ansible\-collections/community\.docker/pull/546](https\://github\.com/ansible\-collections/community\.docker/pull/546)\)\.
* docker\_plugin \- do not crash if plugin is installed in check mode \([https\://github\.com/ansible\-collections/community\.docker/issues/552](https\://github\.com/ansible\-collections/community\.docker/issues/552)\, [https\://github\.com/ansible\-collections/community\.docker/pull/553](https\://github\.com/ansible\-collections/community\.docker/pull/553)\)\.
* most modules \- fix handling of <code>DOCKER\_TIMEOUT</code> environment variable\, and improve handling of other fallback environment variables \([https\://github\.com/ansible\-collections/community\.docker/issues/551](https\://github\.com/ansible\-collections/community\.docker/issues/551)\, [https\://github\.com/ansible\-collections/community\.docker/pull/554](https\://github\.com/ansible\-collections/community\.docker/pull/554)\)\.

<a id="v2-7-3"></a>
## v2\.7\.3

<a id="release-summary-10"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-9"></a>
### Bugfixes

* current\_container\_facts \- make container detection work better in more cases \([https\://github\.com/ansible\-collections/community\.docker/pull/522](https\://github\.com/ansible\-collections/community\.docker/pull/522)\)\.

<a id="v2-7-2"></a>
## v2\.7\.2

<a id="release-summary-11"></a>
### Release Summary

Bugfix release\.

<a id="minor-changes"></a>
### Minor Changes

* current\_container\_facts \- make work with current Docker version \([https\://github\.com/ansible\-collections/community\.docker/pull/510](https\://github\.com/ansible\-collections/community\.docker/pull/510)\, [https\://github\.com/ansible\-collections/community\.docker/pull/512](https\://github\.com/ansible\-collections/community\.docker/pull/512)\)\.

<a id="v2-7-1"></a>
## v2\.7\.1

<a id="release-summary-12"></a>
### Release Summary

Maintenance release with updated documentation\.

<a id="bugfixes-10"></a>
### Bugfixes

* docker\_stack \- fix broken string formatting when reporting error in case <code>compose</code> was containing invalid values \([https\://github\.com/ansible\-collections/community\.docker/pull/448](https\://github\.com/ansible\-collections/community\.docker/pull/448)\)\.

<a id="v2-7-0"></a>
## v2\.7\.0

<a id="release-summary-13"></a>
### Release Summary

Bugfix and deprecation release\. The next 2\.x\.y releases will only be bugfix releases\, the next expect minor/major release will be 3\.0\.0 with some major changes\.

<a id="minor-changes-1"></a>
### Minor Changes

* Move common utility functions from the <code>common</code> module\_util to a new module\_util called <code>util</code>\. This should not have any user\-visible effect \([https\://github\.com/ansible\-collections/community\.docker/pull/390](https\://github\.com/ansible\-collections/community\.docker/pull/390)\)\.

<a id="deprecated-features"></a>
### Deprecated Features

* Support for Docker API version 1\.20 to 1\.24 has been deprecated and will be removed in community\.docker 3\.0\.0\. The first Docker version supporting API version 1\.25 was Docker 1\.13\, released in January 2017\. This affects the modules <code>docker\_container</code>\, <code>docker\_container\_exec</code>\, <code>docker\_container\_info</code>\, <code>docker\_compose</code>\, <code>docker\_login</code>\, <code>docker\_image</code>\, <code>docker\_image\_info</code>\, <code>docker\_image\_load</code>\, <code>docker\_host\_info</code>\, <code>docker\_network</code>\, <code>docker\_network\_info</code>\, <code>docker\_node\_info</code>\, <code>docker\_swarm\_info</code>\, <code>docker\_swarm\_service</code>\, <code>docker\_swarm\_service\_info</code>\, <code>docker\_volume\_info</code>\, and <code>docker\_volume</code>\, whose minimally supported API version is between 1\.20 and 1\.24 \([https\://github\.com/ansible\-collections/community\.docker/pull/396](https\://github\.com/ansible\-collections/community\.docker/pull/396)\)\.
* Support for Python 2\.6 is deprecated and will be removed in the next major release \(community\.docker 3\.0\.0\)\. Some modules might still work with Python 2\.6\, but we will no longer try to ensure compatibility \([https\://github\.com/ansible\-collections/community\.docker/pull/388](https\://github\.com/ansible\-collections/community\.docker/pull/388)\)\.

<a id="bugfixes-11"></a>
### Bugfixes

* Docker SDK for Python based modules and plugins \- if the API version is specified as an option\, use that one to validate API version requirements of module/plugin options instead of the latest API version supported by the Docker daemon\. This also avoids one unnecessary API call per module/plugin \([https\://github\.com/ansible\-collections/community\.docker/pull/389](https\://github\.com/ansible\-collections/community\.docker/pull/389)\)\.

<a id="v2-6-0"></a>
## v2\.6\.0

<a id="release-summary-14"></a>
### Release Summary

Bugfix and feature release\.

<a id="minor-changes-2"></a>
### Minor Changes

* docker\_container \- added <code>image\_label\_mismatch</code> parameter \([https\://github\.com/ansible\-collections/community\.docker/issues/314](https\://github\.com/ansible\-collections/community\.docker/issues/314)\, [https\://github\.com/ansible\-collections/community\.docker/pull/370](https\://github\.com/ansible\-collections/community\.docker/pull/370)\)\.

<a id="deprecated-features-1"></a>
### Deprecated Features

* Support for Ansible 2\.9 and ansible\-base 2\.10 is deprecated\, and will be removed in the next major release \(community\.docker 3\.0\.0\)\. Some modules might still work with these versions afterwards\, but we will no longer keep compatibility code that was needed to support them \([https\://github\.com/ansible\-collections/community\.docker/pull/361](https\://github\.com/ansible\-collections/community\.docker/pull/361)\)\.
* The dependency on docker\-compose for Execution Environments is deprecated and will be removed in community\.docker 3\.0\.0\. The [Python docker\-compose library](https\://pypi\.org/project/docker\-compose/) is unmaintained and can cause dependency issues\. You can manually still install it in an Execution Environment when needed \([https\://github\.com/ansible\-collections/community\.docker/pull/373](https\://github\.com/ansible\-collections/community\.docker/pull/373)\)\.
* Various modules \- the default of <code>tls\_hostname</code> that was supposed to be removed in community\.docker 2\.0\.0 will now be removed in version 3\.0\.0 \([https\://github\.com/ansible\-collections/community\.docker/pull/362](https\://github\.com/ansible\-collections/community\.docker/pull/362)\)\.
* docker\_stack \- the return values <code>out</code> and <code>err</code> that were supposed to be removed in community\.docker 2\.0\.0 will now be removed in version 3\.0\.0 \([https\://github\.com/ansible\-collections/community\.docker/pull/362](https\://github\.com/ansible\-collections/community\.docker/pull/362)\)\.

<a id="bugfixes-12"></a>
### Bugfixes

* docker\_container \- fail with a meaningful message instead of crashing if a port is specified with more than three colon\-separated parts \([https\://github\.com/ansible\-collections/community\.docker/pull/367](https\://github\.com/ansible\-collections/community\.docker/pull/367)\, [https\://github\.com/ansible\-collections/community\.docker/issues/365](https\://github\.com/ansible\-collections/community\.docker/issues/365)\)\.
* docker\_container \- remove unused code that will cause problems with Python 3\.13 \([https\://github\.com/ansible\-collections/community\.docker/pull/354](https\://github\.com/ansible\-collections/community\.docker/pull/354)\)\.

<a id="v2-5-1"></a>
## v2\.5\.1

<a id="release-summary-15"></a>
### Release Summary

Maintenance release\.

<a id="bugfixes-13"></a>
### Bugfixes

* Include <code>PSF\-license\.txt</code> file for <code>plugins/module\_utils/\_version\.py</code>\.

<a id="v2-5-0"></a>
## v2\.5\.0

<a id="release-summary-16"></a>
### Release Summary

Regular feature release\.

<a id="minor-changes-3"></a>
### Minor Changes

* docker\_config \- add support for <code>template\_driver</code> with one option <code>golang</code> \([https\://github\.com/ansible\-collections/community\.docker/issues/332](https\://github\.com/ansible\-collections/community\.docker/issues/332)\, [https\://github\.com/ansible\-collections/community\.docker/pull/345](https\://github\.com/ansible\-collections/community\.docker/pull/345)\)\.
* docker\_swarm \- adds <code>data\_path\_addr</code> parameter during swarm initialization or when joining \([https\://github\.com/ansible\-collections/community\.docker/issues/339](https\://github\.com/ansible\-collections/community\.docker/issues/339)\)\.

<a id="v2-4-0"></a>
## v2\.4\.0

<a id="release-summary-17"></a>
### Release Summary

Regular feature and bugfix release\.

<a id="minor-changes-4"></a>
### Minor Changes

* Prepare collection for inclusion in an Execution Environment by declaring its dependencies\. The <code>docker\_stack\*</code> modules are not supported \([https\://github\.com/ansible\-collections/community\.docker/pull/336](https\://github\.com/ansible\-collections/community\.docker/pull/336)\)\.
* current\_container\_facts \- add detection for GitHub Actions \([https\://github\.com/ansible\-collections/community\.docker/pull/336](https\://github\.com/ansible\-collections/community\.docker/pull/336)\)\.
* docker\_container \- support returning Docker container log output when using Docker\'s <code>local</code> logging driver\, an optimized local logging driver introduced in Docker 18\.09 \([https\://github\.com/ansible\-collections/community\.docker/pull/337](https\://github\.com/ansible\-collections/community\.docker/pull/337)\)\.

<a id="bugfixes-14"></a>
### Bugfixes

* docker connection plugin \- make sure that <code>docker\_extra\_args</code> is used for querying the Docker version\. Also ensures that the Docker version is only queried when needed\. This is currently the case if a remote user is specified \([https\://github\.com/ansible\-collections/community\.docker/issues/325](https\://github\.com/ansible\-collections/community\.docker/issues/325)\, [https\://github\.com/ansible\-collections/community\.docker/pull/327](https\://github\.com/ansible\-collections/community\.docker/pull/327)\)\.

<a id="v2-3-0"></a>
## v2\.3\.0

<a id="release-summary-18"></a>
### Release Summary

Regular feature and bugfix release\.

<a id="minor-changes-5"></a>
### Minor Changes

* docker connection plugin \- implement connection reset by clearing internal container user cache \([https\://github\.com/ansible\-collections/community\.docker/pull/312](https\://github\.com/ansible\-collections/community\.docker/pull/312)\)\.
* docker connection plugin \- simplify <code>actual\_user</code> handling code \([https\://github\.com/ansible\-collections/community\.docker/pull/311](https\://github\.com/ansible\-collections/community\.docker/pull/311)\)\.
* docker connection plugin \- the plugin supports new ways to define the timeout\. These are the <code>ANSIBLE\_DOCKER\_TIMEOUT</code> environment variable\, the <code>timeout</code> setting in the <code>docker\_connection</code> section of <code>ansible\.cfg</code>\, and the <code>ansible\_docker\_timeout</code> variable \([https\://github\.com/ansible\-collections/community\.docker/pull/297](https\://github\.com/ansible\-collections/community\.docker/pull/297)\)\.
* docker\_api connection plugin \- implement connection reset by clearing internal container user/group ID cache \([https\://github\.com/ansible\-collections/community\.docker/pull/312](https\://github\.com/ansible\-collections/community\.docker/pull/312)\)\.
* docker\_api connection plugin \- the plugin supports new ways to define the timeout\. These are the <code>ANSIBLE\_DOCKER\_TIMEOUT</code> environment variable\, the <code>timeout</code> setting in the <code>docker\_connection</code> section of <code>ansible\.cfg</code>\, and the <code>ansible\_docker\_timeout</code> variable \([https\://github\.com/ansible\-collections/community\.docker/pull/308](https\://github\.com/ansible\-collections/community\.docker/pull/308)\)\.

<a id="bugfixes-15"></a>
### Bugfixes

* docker connection plugin \- fix option handling to be compatible with ansible\-core 2\.13 \([https\://github\.com/ansible\-collections/community\.docker/pull/297](https\://github\.com/ansible\-collections/community\.docker/pull/297)\, [https\://github\.com/ansible\-collections/community\.docker/issues/307](https\://github\.com/ansible\-collections/community\.docker/issues/307)\)\.
* docker\_api connection plugin \- fix option handling to be compatible with ansible\-core 2\.13 \([https\://github\.com/ansible\-collections/community\.docker/pull/308](https\://github\.com/ansible\-collections/community\.docker/pull/308)\)\.

<a id="v2-2-1"></a>
## v2\.2\.1

<a id="release-summary-19"></a>
### Release Summary

Regular bugfix release\.

<a id="bugfixes-16"></a>
### Bugfixes

* docker\_compose \- fix Python 3 type error when extracting warnings or errors from docker\-compose\'s output \([https\://github\.com/ansible\-collections/community\.docker/pull/305](https\://github\.com/ansible\-collections/community\.docker/pull/305)\)\.

<a id="v2-2-0"></a>
## v2\.2\.0

<a id="release-summary-20"></a>
### Release Summary

Regular feature and bugfix release\.

<a id="minor-changes-6"></a>
### Minor Changes

* docker\_config \- add support for rolling update\, set <code>rolling\_versions</code> to <code>true</code> to enable \([https\://github\.com/ansible\-collections/community\.docker/pull/295](https\://github\.com/ansible\-collections/community\.docker/pull/295)\, [https\://github\.com/ansible\-collections/community\.docker/issues/109](https\://github\.com/ansible\-collections/community\.docker/issues/109)\)\.
* docker\_secret \- add support for rolling update\, set <code>rolling\_versions</code> to <code>true</code> to enable \([https\://github\.com/ansible\-collections/community\.docker/pull/293](https\://github\.com/ansible\-collections/community\.docker/pull/293)\, [https\://github\.com/ansible\-collections/community\.docker/issues/21](https\://github\.com/ansible\-collections/community\.docker/issues/21)\)\.
* docker\_swarm\_service \- add support for setting capabilities with the <code>cap\_add</code> and <code>cap\_drop</code> parameters\. Usage is the same as with the <code>capabilities</code> and <code>cap\_drop</code> parameters for <code>docker\_container</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/294](https\://github\.com/ansible\-collections/community\.docker/pull/294)\)\.

<a id="bugfixes-17"></a>
### Bugfixes

* docker\_container\, docker\_image \- adjust image finding code to pecularities of <code>podman\-docker</code>\'s API emulation when Docker short names like <code>redis</code> are used \([https\://github\.com/ansible\-collections/community\.docker/issues/292](https\://github\.com/ansible\-collections/community\.docker/issues/292)\)\.

<a id="v2-1-1"></a>
## v2\.1\.1

<a id="release-summary-21"></a>
### Release Summary

Emergency release to amend breaking change in previous release\.

<a id="bugfixes-18"></a>
### Bugfixes

* Fix unintended breaking change caused by [an earlier fix](https\://github\.com/ansible\-collections/community\.docker/pull/258) by vendoring the deprecated Python standard library <code>distutils\.version</code> until this collection stops supporting Ansible 2\.9 and ansible\-base 2\.10 \([https\://github\.com/ansible\-collections/community\.docker/issues/267](https\://github\.com/ansible\-collections/community\.docker/issues/267)\, [https\://github\.com/ansible\-collections/community\.docker/pull/269](https\://github\.com/ansible\-collections/community\.docker/pull/269)\)\.

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="release-summary-22"></a>
### Release Summary

Feature and bugfix release\.

<a id="minor-changes-7"></a>
### Minor Changes

* docker\_container\_exec \- add <code>detach</code> parameter \([https\://github\.com/ansible\-collections/community\.docker/issues/250](https\://github\.com/ansible\-collections/community\.docker/issues/250)\, [https\://github\.com/ansible\-collections/community\.docker/pull/255](https\://github\.com/ansible\-collections/community\.docker/pull/255)\)\.
* docker\_container\_exec \- add <code>env</code> option \([https\://github\.com/ansible\-collections/community\.docker/issues/248](https\://github\.com/ansible\-collections/community\.docker/issues/248)\, [https\://github\.com/ansible\-collections/community\.docker/pull/254](https\://github\.com/ansible\-collections/community\.docker/pull/254)\)\.

<a id="bugfixes-19"></a>
### Bugfixes

* Various modules and plugins \- use vendored version of <code>distutils\.version</code> included in ansible\-core 2\.12 if available\. This avoids breakage when <code>distutils</code> is removed from the standard library of Python 3\.12\. Note that ansible\-core 2\.11\, ansible\-base 2\.10 and Ansible 2\.9 are right now not compatible with Python 3\.12\, hence this fix does not target these ansible\-core/\-base/2\.9 versions \([https\://github\.com/ansible\-collections/community\.docker/pull/258](https\://github\.com/ansible\-collections/community\.docker/pull/258)\)\.
* docker connection plugin \- replace deprecated <code>distutils\.spawn\.find\_executable</code> with Ansible\'s <code>get\_bin\_path</code> to find the <code>docker</code> executable \([https\://github\.com/ansible\-collections/community\.docker/pull/257](https\://github\.com/ansible\-collections/community\.docker/pull/257)\)\.
* docker\_container\_exec \- disallow using the <code>chdir</code> option for Docker API before 1\.35 \([https\://github\.com/ansible\-collections/community\.docker/pull/253](https\://github\.com/ansible\-collections/community\.docker/pull/253)\)\.

<a id="v2-0-2"></a>
## v2\.0\.2

<a id="release-summary-23"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-20"></a>
### Bugfixes

* docker\_api connection plugin \- avoid passing an unnecessary argument to a Docker SDK for Python call that is only supported by version 3\.0\.0 or later \([https\://github\.com/ansible\-collections/community\.docker/pull/243](https\://github\.com/ansible\-collections/community\.docker/pull/243)\)\.
* docker\_container\_exec \- <code>chdir</code> is only supported since Docker SDK for Python 3\.0\.0\. Make sure that this option can only use when 3\.0\.0 or later is installed\, and prevent passing this parameter on when <code>chdir</code> is not provided to this module \([https\://github\.com/ansible\-collections/community\.docker/pull/243](https\://github\.com/ansible\-collections/community\.docker/pull/243)\, [https\://github\.com/ansible\-collections/community\.docker/issues/242](https\://github\.com/ansible\-collections/community\.docker/issues/242)\)\.
* nsenter connection plugin \- ensure the <code>nsenter\_pid</code> option is retrieved in <code>\_connect</code> instead of <code>\_\_init\_\_</code> to prevent a crasher due to bad initialization order \([https\://github\.com/ansible\-collections/community\.docker/pull/249](https\://github\.com/ansible\-collections/community\.docker/pull/249)\)\.
* nsenter connection plugin \- replace the use of <code>\-\-all\-namespaces</code> with specific namespaces to support compatibility with Busybox nsenter \(used on\, for example\, Alpine containers\) \([https\://github\.com/ansible\-collections/community\.docker/pull/249](https\://github\.com/ansible\-collections/community\.docker/pull/249)\)\.

<a id="v2-0-1"></a>
## v2\.0\.1

<a id="release-summary-24"></a>
### Release Summary

Maintenance release with some documentation fixes\.

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="release-summary-25"></a>
### Release Summary

New major release with some deprecations removed and a breaking change in the <code>docker\_compose</code> module regarding the <code>timeout</code> parameter\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* docker\_compose \- fixed <code>timeout</code> defaulting behavior so that <code>stop\_grace\_period</code>\, if defined in the compose file\, will be used if <em class="title-reference">timeout\`</em> is not specified \([https\://github\.com/ansible\-collections/community\.docker/pull/163](https\://github\.com/ansible\-collections/community\.docker/pull/163)\)\.

<a id="deprecated-features-2"></a>
### Deprecated Features

* docker\_container \- using the special value <code>all</code> in <code>published\_ports</code> has been deprecated\. Use <code>publish\_all\_ports\=true</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/210](https\://github\.com/ansible\-collections/community\.docker/pull/210)\)\.

<a id="removed-features-previously-deprecated"></a>
### Removed Features \(previously deprecated\)

* docker\_container \- the default value of <code>container\_default\_behavior</code> changed to <code>no\_defaults</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/210](https\://github\.com/ansible\-collections/community\.docker/pull/210)\)\.
* docker\_container \- the default value of <code>network\_mode</code> is now the name of the first network specified in <code>networks</code> if such are specified and <code>networks\_cli\_compatible\=true</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/210](https\://github\.com/ansible\-collections/community\.docker/pull/210)\)\.
* docker\_container \- the special value <code>all</code> can no longer be used in <code>published\_ports</code> next to other values\. Please use <code>publish\_all\_ports\=true</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/210](https\://github\.com/ansible\-collections/community\.docker/pull/210)\)\.
* docker\_login \- removed the <code>email</code> option \([https\://github\.com/ansible\-collections/community\.docker/pull/210](https\://github\.com/ansible\-collections/community\.docker/pull/210)\)\.

<a id="v1-10-0"></a>
## v1\.10\.0

<a id="release-summary-26"></a>
### Release Summary

Regular feature and bugfix release\.

<a id="minor-changes-8"></a>
### Minor Changes

* Add the modules docker\_container\_exec\, docker\_image\_load and docker\_plugin to the <code>docker</code> module defaults group \([https\://github\.com/ansible\-collections/community\.docker/pull/209](https\://github\.com/ansible\-collections/community\.docker/pull/209)\)\.
* docker\_config \- add option <code>data\_src</code> to read configuration data from target \([https\://github\.com/ansible\-collections/community\.docker/issues/64](https\://github\.com/ansible\-collections/community\.docker/issues/64)\, [https\://github\.com/ansible\-collections/community\.docker/pull/203](https\://github\.com/ansible\-collections/community\.docker/pull/203)\)\.
* docker\_secret \- add option <code>data\_src</code> to read secret data from target \([https\://github\.com/ansible\-collections/community\.docker/issues/64](https\://github\.com/ansible\-collections/community\.docker/issues/64)\, [https\://github\.com/ansible\-collections/community\.docker/pull/203](https\://github\.com/ansible\-collections/community\.docker/pull/203)\)\.

<a id="v1-9-1"></a>
## v1\.9\.1

<a id="release-summary-27"></a>
### Release Summary

Regular bugfix release\.

<a id="bugfixes-21"></a>
### Bugfixes

* docker\_compose \- fixed incorrect <code>changed</code> status for services with <code>profiles</code> defined\, but none enabled \([https\://github\.com/ansible\-collections/community\.docker/pull/192](https\://github\.com/ansible\-collections/community\.docker/pull/192)\)\.

<a id="v1-9-0"></a>
## v1\.9\.0

<a id="release-summary-28"></a>
### Release Summary

New bugfixes and features release\.

<a id="minor-changes-9"></a>
### Minor Changes

* docker\_\* modules \- include <code>ImportError</code> traceback when reporting that Docker SDK for Python could not be found \([https\://github\.com/ansible\-collections/community\.docker/pull/188](https\://github\.com/ansible\-collections/community\.docker/pull/188)\)\.
* docker\_compose \- added <code>env\_file</code> option for specifying custom environment files \([https\://github\.com/ansible\-collections/community\.docker/pull/174](https\://github\.com/ansible\-collections/community\.docker/pull/174)\)\.
* docker\_container \- added <code>publish\_all\_ports</code> option to publish all exposed ports to random ports except those explicitly bound with <code>published\_ports</code> \(this was already added in community\.docker 1\.8\.0\) \([https\://github\.com/ansible\-collections/community\.docker/pull/162](https\://github\.com/ansible\-collections/community\.docker/pull/162)\)\.
* docker\_container \- added new <code>command\_handling</code> option with current deprecated default value <code>compatibility</code> which allows to control how the module handles shell quoting when interpreting lists\, and how the module handles empty lists/strings\. The default will switch to <code>correct</code> in community\.docker 3\.0\.0 \([https\://github\.com/ansible\-collections/community\.docker/pull/186](https\://github\.com/ansible\-collections/community\.docker/pull/186)\)\.
* docker\_container \- lifted restriction preventing the creation of anonymous volumes with the <code>mounts</code> option \([https\://github\.com/ansible\-collections/community\.docker/pull/181](https\://github\.com/ansible\-collections/community\.docker/pull/181)\)\.

<a id="deprecated-features-3"></a>
### Deprecated Features

* docker\_container \- the new <code>command\_handling</code>\'s default value\, <code>compatibility</code>\, is deprecated and will change to <code>correct</code> in community\.docker 3\.0\.0\. A deprecation warning is emitted by the module in cases where the behavior will change\. Please note that ansible\-core will output a deprecation warning only once\, so if it is shown for an earlier task\, there could be more tasks with this warning where it is not shown \([https\://github\.com/ansible\-collections/community\.docker/pull/186](https\://github\.com/ansible\-collections/community\.docker/pull/186)\)\.

<a id="bugfixes-22"></a>
### Bugfixes

* docker\_compose \- fixes task failures when bringing up services while using <code>docker\-compose \<1\.17\.0</code> \([https\://github\.com/ansible\-collections/community\.docker/issues/180](https\://github\.com/ansible\-collections/community\.docker/issues/180)\)\.
* docker\_container \- make sure to also return <code>container</code> on <code>detached\=false</code> when status code is non\-zero \([https\://github\.com/ansible\-collections/community\.docker/pull/178](https\://github\.com/ansible\-collections/community\.docker/pull/178)\)\.
* docker\_stack\_info \- make sure that module isn\'t skipped in check mode \([https\://github\.com/ansible\-collections/community\.docker/pull/183](https\://github\.com/ansible\-collections/community\.docker/pull/183)\)\.
* docker\_stack\_task\_info \- make sure that module isn\'t skipped in check mode \([https\://github\.com/ansible\-collections/community\.docker/pull/183](https\://github\.com/ansible\-collections/community\.docker/pull/183)\)\.

<a id="new-plugins"></a>
### New Plugins

<a id="connection"></a>
#### Connection

* nsenter \- execute on host running controller container

<a id="v1-8-0"></a>
## v1\.8\.0

<a id="release-summary-29"></a>
### Release Summary

Regular bugfix and feature release\.

<a id="minor-changes-10"></a>
### Minor Changes

* Avoid internal ansible\-core module\_utils in favor of equivalent public API available since at least Ansible 2\.9 \([https\://github\.com/ansible\-collections/community\.docker/pull/164](https\://github\.com/ansible\-collections/community\.docker/pull/164)\)\.
* docker\_compose \- added <code>profiles</code> option to specify service profiles when starting services \([https\://github\.com/ansible\-collections/community\.docker/pull/167](https\://github\.com/ansible\-collections/community\.docker/pull/167)\)\.
* docker\_containers inventory plugin \- when <code>connection\_type\=docker\-api</code>\, now pass Docker daemon connection options from inventory plugin to connection plugin\. This can be disabled by setting <code>configure\_docker\_daemon\=false</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/157](https\://github\.com/ansible\-collections/community\.docker/pull/157)\)\.
* docker\_host\_info \- allow values for keys in <code>containers\_filters</code>\, <code>images\_filters</code>\, <code>networks\_filters</code>\, and <code>volumes\_filters</code> to be passed as YAML lists \([https\://github\.com/ansible\-collections/community\.docker/pull/160](https\://github\.com/ansible\-collections/community\.docker/pull/160)\)\.
* docker\_plugin \- added <code>alias</code> option to specify local names for docker plugins \([https\://github\.com/ansible\-collections/community\.docker/pull/161](https\://github\.com/ansible\-collections/community\.docker/pull/161)\)\.

<a id="bugfixes-23"></a>
### Bugfixes

* docker\_compose \- fix idempotence bug when using <code>stopped\: true</code> \([https\://github\.com/ansible\-collections/community\.docker/issues/142](https\://github\.com/ansible\-collections/community\.docker/issues/142)\, [https\://github\.com/ansible\-collections/community\.docker/pull/159](https\://github\.com/ansible\-collections/community\.docker/pull/159)\)\.

<a id="v1-7-0"></a>
## v1\.7\.0

<a id="release-summary-30"></a>
### Release Summary

Small feature and bugfix release\.

<a id="minor-changes-11"></a>
### Minor Changes

* docker\_image \- allow to tag images by ID \([https\://github\.com/ansible\-collections/community\.docker/pull/149](https\://github\.com/ansible\-collections/community\.docker/pull/149)\)\.

<a id="v1-6-1"></a>
## v1\.6\.1

<a id="release-summary-31"></a>
### Release Summary

Bugfix release to reduce deprecation warning spam\.

<a id="bugfixes-24"></a>
### Bugfixes

* docker\_\* modules and plugins\, except <code>docker\_swarm</code> connection plugin and <code>docker\_compose</code> and <code>docker\_stack\*\` modules \- only emit \`\`tls\_hostname</code> deprecation message if TLS is actually used \([https\://github\.com/ansible\-collections/community\.docker/pull/143](https\://github\.com/ansible\-collections/community\.docker/pull/143)\)\.

<a id="v1-6-0"></a>
## v1\.6\.0

<a id="release-summary-32"></a>
### Release Summary

Regular bugfix and feature release\.

<a id="minor-changes-12"></a>
### Minor Changes

* common module utils \- correct error messages for guiding to install proper Docker SDK for Python module \([https\://github\.com/ansible\-collections/community\.docker/pull/125](https\://github\.com/ansible\-collections/community\.docker/pull/125)\)\.
* docker\_container \- allow <code>memory\_swap\: \-1</code> to set memory swap limit to unlimited\. This is useful when the user cannot set memory swap limits due to cgroup limitations or other reasons\, as by default Docker will try to set swap usage to two times the value of <code>memory</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/138](https\://github\.com/ansible\-collections/community\.docker/pull/138)\)\.

<a id="deprecated-features-4"></a>
### Deprecated Features

* docker\_\* modules and plugins\, except <code>docker\_swarm</code> connection plugin and <code>docker\_compose</code> and <code>docker\_stack\*\` modules \- the current default \`\`localhost</code> for <code>tls\_hostname</code> is deprecated\. In community\.docker 2\.0\.0 it will be computed from <code>docker\_host</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/134](https\://github\.com/ansible\-collections/community\.docker/pull/134)\)\.

<a id="bugfixes-25"></a>
### Bugfixes

* docker\-compose \- fix not pulling when <code>state\: present</code> and <code>stopped\: true</code> \([https\://github\.com/ansible\-collections/community\.docker/issues/12](https\://github\.com/ansible\-collections/community\.docker/issues/12)\, [https\://github\.com/ansible\-collections/community\.docker/pull/119](https\://github\.com/ansible\-collections/community\.docker/pull/119)\)\.
* docker\_plugin \- also configure plugin after installing \([https\://github\.com/ansible\-collections/community\.docker/issues/118](https\://github\.com/ansible\-collections/community\.docker/issues/118)\, [https\://github\.com/ansible\-collections/community\.docker/pull/135](https\://github\.com/ansible\-collections/community\.docker/pull/135)\)\.
* docker\_swarm\_services \- avoid crash during idempotence check if <code>published\_port</code> is not specified \([https\://github\.com/ansible\-collections/community\.docker/issues/107](https\://github\.com/ansible\-collections/community\.docker/issues/107)\, [https\://github\.com/ansible\-collections/community\.docker/pull/136](https\://github\.com/ansible\-collections/community\.docker/pull/136)\)\.

<a id="v1-5-0"></a>
## v1\.5\.0

<a id="release-summary-33"></a>
### Release Summary

Regular feature release\.

<a id="minor-changes-13"></a>
### Minor Changes

* Add the <code>use\_ssh\_client</code> option to most docker modules and plugins \([https\://github\.com/ansible\-collections/community\.docker/issues/108](https\://github\.com/ansible\-collections/community\.docker/issues/108)\, [https\://github\.com/ansible\-collections/community\.docker/pull/114](https\://github\.com/ansible\-collections/community\.docker/pull/114)\)\.

<a id="bugfixes-26"></a>
### Bugfixes

* all modules \- use <code>to\_native</code> to convert exceptions to strings \([https\://github\.com/ansible\-collections/community\.docker/pull/121](https\://github\.com/ansible\-collections/community\.docker/pull/121)\)\.

<a id="new-modules"></a>
### New Modules

* docker\_container\_exec \- Execute command in a docker container

<a id="v1-4-0"></a>
## v1\.4\.0

<a id="release-summary-34"></a>
### Release Summary

Security release to address another potential secret leak\. Also includes regular bugfixes and features\.

<a id="minor-changes-14"></a>
### Minor Changes

* docker\_swarm\_service \- change <code>publish\.published\_port</code> option from mandatory to optional\. Docker will assign random high port if not specified \([https\://github\.com/ansible\-collections/community\.docker/issues/99](https\://github\.com/ansible\-collections/community\.docker/issues/99)\)\.

<a id="breaking-changes--porting-guide-1"></a>
### Breaking Changes / Porting Guide

* docker\_swarm \- if <code>join\_token</code> is specified\, a returned join token with the same value will be replaced by <code>VALUE\_SPECIFIED\_IN\_NO\_LOG\_PARAMETER</code>\. Make sure that you do not blindly use the join tokens from the return value of this module when the module is invoked with <code>join\_token</code> specified\! This breaking change appears in a minor release since it is necessary to fix a security issue \([https\://github\.com/ansible\-collections/community\.docker/pull/103](https\://github\.com/ansible\-collections/community\.docker/pull/103)\)\.

<a id="security-fixes-1"></a>
### Security Fixes

* docker\_swarm \- the <code>join\_token</code> option is now marked as <code>no\_log</code> so it is no longer written into logs \([https\://github\.com/ansible\-collections/community\.docker/pull/103](https\://github\.com/ansible\-collections/community\.docker/pull/103)\)\.

<a id="bugfixes-27"></a>
### Bugfixes

* <code>docker\_swarm\_service</code> \- fix KeyError on caused by reference to deprecated option <code>update\_failure\_action</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/100](https\://github\.com/ansible\-collections/community\.docker/pull/100)\)\.
* docker\_swarm\_service \- mark <code>secrets</code> module option with <code>no\_log\=False</code> since it does not leak secrets \([https\://github\.com/ansible\-collections/community\.general/pull/2001](https\://github\.com/ansible\-collections/community\.general/pull/2001)\)\.

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="release-summary-35"></a>
### Release Summary

Regular feature and bugfix release\.

<a id="minor-changes-15"></a>
### Minor Changes

* docker\_container \- add <code>storage\_opts</code> option to specify storage options \([https\://github\.com/ansible\-collections/community\.docker/issues/91](https\://github\.com/ansible\-collections/community\.docker/issues/91)\, [https\://github\.com/ansible\-collections/community\.docker/pull/93](https\://github\.com/ansible\-collections/community\.docker/pull/93)\)\.
* docker\_image \- allows to specify platform to pull for <code>source\=pull</code> with new option <code>pull\_platform</code> \([https\://github\.com/ansible\-collections/community\.docker/issues/79](https\://github\.com/ansible\-collections/community\.docker/issues/79)\, [https\://github\.com/ansible\-collections/community\.docker/pull/89](https\://github\.com/ansible\-collections/community\.docker/pull/89)\)\.
* docker\_image \- properly support image IDs \(hashes\) for loading and tagging images \([https\://github\.com/ansible\-collections/community\.docker/issues/86](https\://github\.com/ansible\-collections/community\.docker/issues/86)\, [https\://github\.com/ansible\-collections/community\.docker/pull/87](https\://github\.com/ansible\-collections/community\.docker/pull/87)\)\.
* docker\_swarm\_service \- adding support for maximum number of tasks per node \(<code>replicas\_max\_per\_node</code>\) when running swarm service in replicated mode\. Introduced in API 1\.40 \([https\://github\.com/ansible\-collections/community\.docker/issues/7](https\://github\.com/ansible\-collections/community\.docker/issues/7)\, [https\://github\.com/ansible\-collections/community\.docker/pull/92](https\://github\.com/ansible\-collections/community\.docker/pull/92)\)\.

<a id="bugfixes-28"></a>
### Bugfixes

* docker\_container \- fix healthcheck disabling idempotency issue with strict comparison \([https\://github\.com/ansible\-collections/community\.docker/issues/85](https\://github\.com/ansible\-collections/community\.docker/issues/85)\)\.
* docker\_image \- prevent module failure when removing image that is removed between inspection and removal \([https\://github\.com/ansible\-collections/community\.docker/pull/87](https\://github\.com/ansible\-collections/community\.docker/pull/87)\)\.
* docker\_image \- prevent module failure when removing non\-existant image by ID \([https\://github\.com/ansible\-collections/community\.docker/pull/87](https\://github\.com/ansible\-collections/community\.docker/pull/87)\)\.
* docker\_image\_info \- prevent module failure when image vanishes between listing and inspection \([https\://github\.com/ansible\-collections/community\.docker/pull/87](https\://github\.com/ansible\-collections/community\.docker/pull/87)\)\.
* docker\_image\_info \- prevent module failure when querying non\-existant image by ID \([https\://github\.com/ansible\-collections/community\.docker/pull/87](https\://github\.com/ansible\-collections/community\.docker/pull/87)\)\.

<a id="new-modules-1"></a>
### New Modules

* docker\_image\_load \- Load docker image\(s\) from archives
* docker\_plugin \- Manage Docker plugins

<a id="v1-2-2"></a>
## v1\.2\.2

<a id="release-summary-36"></a>
### Release Summary

Security bugfix release to address CVE\-2021\-20191\.

<a id="security-fixes-2"></a>
### Security Fixes

* docker\_swarm \- enabled <code>no\_log</code> for the option <code>signing\_ca\_key</code> to prevent accidental disclosure \(CVE\-2021\-20191\, [https\://github\.com/ansible\-collections/community\.docker/pull/80](https\://github\.com/ansible\-collections/community\.docker/pull/80)\)\.

<a id="v1-2-1"></a>
## v1\.2\.1

<a id="release-summary-37"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-29"></a>
### Bugfixes

* docker connection plugin \- fix Docker version parsing\, as some docker versions have a leading <code>v</code> in the output of the command <code>docker version \-\-format \"\{\{\.Server\.Version\}\}\"</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/76](https\://github\.com/ansible\-collections/community\.docker/pull/76)\)\.

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="release-summary-38"></a>
### Release Summary

Feature release with one new feature and two bugfixes\.

<a id="minor-changes-16"></a>
### Minor Changes

* docker\_container \- added <code>default\_host\_ip</code> option which allows to explicitly set the default IP string for published ports without explicitly specified IPs\. When using IPv6 binds with Docker 20\.10\.2 or newer\, this needs to be set to an empty string \(<code>\"\"</code>\) \([https\://github\.com/ansible\-collections/community\.docker/issues/70](https\://github\.com/ansible\-collections/community\.docker/issues/70)\, [https\://github\.com/ansible\-collections/community\.docker/pull/71](https\://github\.com/ansible\-collections/community\.docker/pull/71)\)\.

<a id="bugfixes-30"></a>
### Bugfixes

* docker\_container \- allow IPv6 zones \(RFC 4007\) in bind IPs \([https\://github\.com/ansible\-collections/community\.docker/pull/66](https\://github\.com/ansible\-collections/community\.docker/pull/66)\)\.
* docker\_image \- fix crash on loading images with versions of Docker SDK for Python before 2\.5\.0 \([https\://github\.com/ansible\-collections/community\.docker/issues/72](https\://github\.com/ansible\-collections/community\.docker/issues/72)\, [https\://github\.com/ansible\-collections/community\.docker/pull/73](https\://github\.com/ansible\-collections/community\.docker/pull/73)\)\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary-39"></a>
### Release Summary

Feature release with three new plugins and modules\.

<a id="minor-changes-17"></a>
### Minor Changes

* docker\_container \- support specifying <code>cgroup\_parent</code> \([https\://github\.com/ansible\-collections/community\.docker/issues/6](https\://github\.com/ansible\-collections/community\.docker/issues/6)\, [https\://github\.com/ansible\-collections/community\.docker/pull/59](https\://github\.com/ansible\-collections/community\.docker/pull/59)\)\.
* docker\_container \- when a container is started with <code>detached\=false</code>\, <code>status</code> is now also returned when it is 0 \([https\://github\.com/ansible\-collections/community\.docker/issues/26](https\://github\.com/ansible\-collections/community\.docker/issues/26)\, [https\://github\.com/ansible\-collections/community\.docker/pull/58](https\://github\.com/ansible\-collections/community\.docker/pull/58)\)\.
* docker\_image \- support <code>platform</code> when building images \([https\://github\.com/ansible\-collections/community\.docker/issues/22](https\://github\.com/ansible\-collections/community\.docker/issues/22)\, [https\://github\.com/ansible\-collections/community\.docker/pull/54](https\://github\.com/ansible\-collections/community\.docker/pull/54)\)\.

<a id="deprecated-features-5"></a>
### Deprecated Features

* docker\_container \- currently <code>published\_ports</code> can contain port mappings next to the special value <code>all</code>\, in which case the port mappings are ignored\. This behavior is deprecated for community\.docker 2\.0\.0\, at which point it will either be forbidden\, or this behavior will be properly implemented similar to how the Docker CLI tool handles this \([https\://github\.com/ansible\-collections/community\.docker/issues/8](https\://github\.com/ansible\-collections/community\.docker/issues/8)\, [https\://github\.com/ansible\-collections/community\.docker/pull/60](https\://github\.com/ansible\-collections/community\.docker/pull/60)\)\.

<a id="bugfixes-31"></a>
### Bugfixes

* docker\_image \- if <code>push\=true</code> is used with <code>repository</code>\, and the image does not need to be tagged\, still push\. This can happen if <code>repository</code> and <code>name</code> are equal \([https\://github\.com/ansible\-collections/community\.docker/issues/52](https\://github\.com/ansible\-collections/community\.docker/issues/52)\, [https\://github\.com/ansible\-collections/community\.docker/pull/53](https\://github\.com/ansible\-collections/community\.docker/pull/53)\)\.
* docker\_image \- report error when loading a broken archive that contains no image \([https\://github\.com/ansible\-collections/community\.docker/issues/46](https\://github\.com/ansible\-collections/community\.docker/issues/46)\, [https\://github\.com/ansible\-collections/community\.docker/pull/55](https\://github\.com/ansible\-collections/community\.docker/pull/55)\)\.
* docker\_image \- report error when the loaded archive does not contain the specified image \([https\://github\.com/ansible\-collections/community\.docker/issues/41](https\://github\.com/ansible\-collections/community\.docker/issues/41)\, [https\://github\.com/ansible\-collections/community\.docker/pull/55](https\://github\.com/ansible\-collections/community\.docker/pull/55)\)\.

<a id="new-plugins-1"></a>
### New Plugins

<a id="connection-1"></a>
#### Connection

* docker\_api \- Run tasks in docker containers

<a id="inventory"></a>
#### Inventory

* docker\_containers \- Ansible dynamic inventory plugin for Docker containers\.

<a id="new-modules-2"></a>
### New Modules

* current\_container\_facts \- Return facts about whether the module runs in a Docker container

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="release-summary-40"></a>
### Release Summary

Maintenance release with a bugfix for <code>docker\_container</code>\.

<a id="bugfixes-32"></a>
### Bugfixes

* docker\_container \- the validation for <code>capabilities</code> in <code>device\_requests</code> was incorrect \([https\://github\.com/ansible\-collections/community\.docker/issues/42](https\://github\.com/ansible\-collections/community\.docker/issues/42)\, [https\://github\.com/ansible\-collections/community\.docker/pull/43](https\://github\.com/ansible\-collections/community\.docker/pull/43)\)\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-41"></a>
### Release Summary

This is the first production \(non\-prerelease\) release of <code>community\.docker</code>\.

<a id="minor-changes-18"></a>
### Minor Changes

* Add collection\-side support of the <code>docker</code> action group / module defaults group \([https\://github\.com/ansible\-collections/community\.docker/pull/17](https\://github\.com/ansible\-collections/community\.docker/pull/17)\)\.
* docker\_image \- return docker build output \([https\://github\.com/ansible\-collections/community\.general/pull/805](https\://github\.com/ansible\-collections/community\.general/pull/805)\)\.
* docker\_secret \- add a warning when the secret does not have an <code>ansible\_key</code> label but the <code>force</code> parameter is not set \([https\://github\.com/ansible\-collections/community\.docker/issues/30](https\://github\.com/ansible\-collections/community\.docker/issues/30)\, [https\://github\.com/ansible\-collections/community\.docker/pull/31](https\://github\.com/ansible\-collections/community\.docker/pull/31)\)\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary-42"></a>
### Release Summary

The <code>community\.docker</code> continues the work on the Ansible docker modules and plugins from their state in <code>community\.general</code> 1\.2\.0\. The changes listed here are thus relative to the modules and plugins <code>community\.general\.docker\*</code>\.

All deprecation removals planned for <code>community\.general</code> 2\.0\.0 have been applied\. All deprecation removals scheduled for <code>community\.general</code> 3\.0\.0 have been re\-scheduled for <code>community\.docker</code> 2\.0\.0\.

<a id="minor-changes-19"></a>
### Minor Changes

* docker\_container \- now supports the <code>device\_requests</code> option\, which allows to request additional resources such as GPUs \([https\://github\.com/ansible/ansible/issues/65748](https\://github\.com/ansible/ansible/issues/65748)\, [https\://github\.com/ansible\-collections/community\.general/pull/1119](https\://github\.com/ansible\-collections/community\.general/pull/1119)\)\.

<a id="removed-features-previously-deprecated-1"></a>
### Removed Features \(previously deprecated\)

* docker\_container \- no longer returns <code>ansible\_facts</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_container \- the default of <code>networks\_cli\_compatible</code> changed to <code>true</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_container \- the unused option <code>trust\_image\_content</code> has been removed \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_image \- <code>state\=build</code> has been removed\. Use <code>present</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_image \- the <code>container\_limits</code>\, <code>dockerfile</code>\, <code>http\_timeout</code>\, <code>nocache</code>\, <code>rm</code>\, <code>path</code>\, <code>buildargs</code>\, <code>pull</code> have been removed\. Use the corresponding suboptions of <code>build</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_image \- the <code>force</code> option has been removed\. Use the more specific <code>force\_\*</code> options instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_image \- the <code>source</code> option is now mandatory \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_image \- the <code>use\_tls</code> option has been removed\. Use <code>tls</code> and <code>validate\_certs</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_image \- the default of the <code>build\.pull</code> option changed to <code>false</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_image\_facts \- this alias is on longer availabe\, use <code>docker\_image\_info</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_network \- no longer returns <code>ansible\_facts</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_network \- the <code>ipam\_options</code> option has been removed\. Use <code>ipam\_config</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_service \- no longer returns <code>ansible\_facts</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_swarm \- <code>state\=inspect</code> has been removed\. Use <code>docker\_swarm\_info</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_swarm\_service \- the <code>constraints</code> option has been removed\. Use <code>placement\.constraints</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_swarm\_service \- the <code>limit\_cpu</code> and <code>limit\_memory</code> options has been removed\. Use the corresponding suboptions in <code>limits</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_swarm\_service \- the <code>log\_driver</code> and <code>log\_driver\_options</code> options has been removed\. Use the corresponding suboptions in <code>logging</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_swarm\_service \- the <code>reserve\_cpu</code> and <code>reserve\_memory</code> options has been removed\. Use the corresponding suboptions in <code>reservations</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_swarm\_service \- the <code>restart\_policy</code>\, <code>restart\_policy\_attempts</code>\, <code>restart\_policy\_delay</code> and <code>restart\_policy\_window</code> options has been removed\. Use the corresponding suboptions in <code>restart\_config</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_swarm\_service \- the <code>update\_delay</code>\, <code>update\_parallelism</code>\, <code>update\_failure\_action</code>\, <code>update\_monitor</code>\, <code>update\_max\_failure\_ratio</code> and <code>update\_order</code> options has been removed\. Use the corresponding suboptions in <code>update\_config</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_volume \- no longer returns <code>ansible\_facts</code> \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.
* docker\_volume \- the <code>force</code> option has been removed\. Use <code>recreate</code> instead \([https\://github\.com/ansible\-collections/community\.docker/pull/1](https\://github\.com/ansible\-collections/community\.docker/pull/1)\)\.

<a id="bugfixes-33"></a>
### Bugfixes

* docker\_login \- fix internal config file storage to handle credentials for more than one registry \([https\://github\.com/ansible\-collections/community\.general/issues/1117](https\://github\.com/ansible\-collections/community\.general/issues/1117)\)\.
