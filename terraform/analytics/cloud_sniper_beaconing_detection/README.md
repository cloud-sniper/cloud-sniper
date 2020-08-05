![alt text](../../../images/logo.png "Cloud Sniper")
<br> </br>
## *Cloud Sniper Beaconing detection*

In order to detect the periodicity in VPC Flow logs packages, we made an adaptation of the `signal-processing` module, part of the project [Signal-Processing](https://github.com/geofizx/Signal-Processing). This other project is also released under a MIT license.

To detect beaconing, we make use of Fourier transforms to detect candidates and then we filter possible false positives from those candidates. The main problem that, due to the nature of VPC Flow logs and the way how data is cached and dumped, the time series obtained for each set of communications between two endpoints is very noisy.

Currently, the lambda zip package is available under the `target` folder. The following dependencies are included in the lambda package:
* numpy
* scipy
* ipaddress
* pandas
