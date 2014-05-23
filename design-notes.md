### Sensors and other domain-based sim data consumers

Vehicles send snapshots of themselves along with a translate event. The snapshot will form part of the event data. Other
data points will be when the event occurred (in sim time) so that the handling of the events doesn't have to be restricted
to the order of generation of the same.

A sensor, having registered its position with the sensor process, will be notified  by the sensor process that it
should have detected a vehicle at a particular time (sim time). The sensor will then do whatever it wants with the data
(aggregation over time, sending to the master sensor, generating reports, put its results on another queue, whatever)


### Distribution of vehicle translation load

We should have processes equal to the number of cpu available. <code>multiprocessing.cpu_count()</code>. If the process
assignment is as follows (each bullet with a process):

- Event dispatcher (sim loop)
- Sensors and reporting to external consumers
- Traffic data listener for vehicles (data coming from another service)

Then, we should distribute the translation of vehicles among about __4 processes__. Translation should be based on edges
and not vehicles or lanes so we avoid sharing state between processes.

### Web workers for the programmable visualiser
http://www.htmlgoodies.com/html5/tutorials/introducing-html-5-web-workers-bringing-multi-threading-to-javascript.html#fbid=b8fvyB-675Y







