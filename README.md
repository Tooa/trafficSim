TrafficSim
=======

Pedestrian traffic simulation with different maps and
predefined simulations like the famous christmas fair simulation.

Getting started
---------------

To run the simulation you need to have at least `Python 3.4` installed. The application
also requires `numpy` and `matplotlib`. You can use `pip` to
resolve the dependencies:

`pip install -r requirements.txt`.



Usage - In a Nutshell
-----

To start a simulation you need to run `simulation.py` with an appropriate simulation file.
Predefined simulations can be found in the `simulations` folder.

`./simulation.py simulations/simple.sim`

####Loveparade simulation

![Simulation Example](https://raw.github.com/tooa/trafficSim/master/example.png)

####Christmas fair simulation

![Simulation Example](https://raw.github.com/tooa/trafficSim/master/example2.png)


Create simulations
-----

| Fieldname   |      Datatype      |  Optional? | Description |
|-------------|:------------------:|------------|------------ |
| name        |  string            | no         | Simulation name |
| psway       |  integer           | no         | Probability that a walker goes off track from the shortest path |
| step_interval        |  integer            | no         | Time between simulation steps in ms |
| mapfile        |  string            | no         | Name of the associated map file without simulation path |
| targets       |  list           | no         | List of all targets. At least one!|
| walkers       |  list           | no         | List of all walker|
| num_rnd_walkers       |  integer           | yes         | Number of random distributed walker. Set to zero to disable |
| rnd_walkers_target        |  string            | yes         | Target of random spawned walker. Leave blank for a random target |
| rnd_walkers_direction        |  integer            | yes         | Start direction that random spawned walker will follow. Leave blank for a random start direction  |
| rnd_walkers_time_min        |  integer            | no         | Determines the minimum time steps for a random walker to follow its start direction |
| rnd_walkers_time_max        |  integer            | no         | Determines the maximum time steps for a random walker to follow its start direction |







License
-------

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
