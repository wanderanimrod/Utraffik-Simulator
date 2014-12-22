## Relaying snapshots

Vehicle snapshots are generated much faster than a snapshot relayer on a separate thread (on the same translator process)
 can write them to redis.
 
Options:

    1. Have more threads writing snapshots to redis, each with its own queue. Make the snapshot relayer put snapshots on the
    writers' queues in a round robbin fashion.
    2. Put the snapshot writer on another process.
    
   
   
Running writer on a queue on the same translator process takes about 5.2seconds. 2 cars.  