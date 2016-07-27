# ambari_custom_alerts

The ambari_agent_heap ambari alert is mainly for demonstrating how to quickly add an Ambari alert.

Here is the way to deploy it : 

* copy the ambari_agent_heap.py file to /var/lib/ambari-server/resources/host_scripts/
* restart ambari-server so that the python script is deployed on every ambari agent
* get the alert.json in your current path and submit it to ambari :

````
[root@]# curl -u admin:admin -i -H 'X-Requested-By:ambari' -X POST -d @alert.json http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/alert_definitions
````

And... well, that's all !
