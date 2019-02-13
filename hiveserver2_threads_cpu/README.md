# HiveServer2 Threads CPU alert

May be useful for identifying if some threads are using a lot of CPU usage. You'll eventually make some jstacks to identify which thread is blocked to understant/address the issue.

* copy the alert_hiveserver2_thread.py file to /var/lib/ambari-server/resources/common-services/HIVE/0.12.0.2.0/package/alerts/
* restart ambari-server so that the python script is deployed on every ambari agent
* get the alert_hiveserver2_thread.json in your current path, modify the cluster name accordingly in the json and submit it to ambari :

````
[root@]# curl -u admin:admin -i -H 'X-Requested-By:ambari' -X POST -d @alert_hiveserver2_thread.json http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/alert_definitions
````
