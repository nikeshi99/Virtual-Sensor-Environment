import time
import paho.mqtt.client as paho
import numpy as np
from threading import Thread

fast_simulate=False

group_id = 'group04m'

broker = '5g-vue.projects.uom.lk'
port = 1883
username = 'iot_user'
password = 'iot@1234'
client_id = group_id

sensor_parameters={ 'temperature-low':18 ,'temperature-high' : 35 , 'humidity-low': 0, 'humidity-high': 100, 'power-consumption-low': 50, 'power-consumption-high': 5000}

# For Temperature Sensor,Humidity sensor, Power Consumption
def periodic_sensor(typ,num,low,high,div,t):
    if fast_simulate:t=t//10
    
    rng = np.random.default_rng()
    val, = rng.integers(low, high, size=1)  
    val_temp = val
    topic='/{}/{}{}'.format(group_id,typ,num)
        
    print(topic)
            
    while(1):
   
        print(typ,end=' ')         
        
        val_temp,=rng.integers(low, high, size=1)    

        val = 0.8*val + 0.2*val_temp
        if val < low:
            val = low
        elif val>high:
            val=high
        print(val,'rand',val_temp)
        client.publish(topic, val,1) 
        time.sleep(t)

# For Motion sensor
def motion_sensor(num):
    if fast_simulate:sim_fact=1
    else: sim_fact=10

    rng = np.random.default_rng()
    topic='/{}/motn{}'.format(group_id,num)
    print(topic)
     
    while(1):
        rand_time, = rng.integers(5, 20, size=1)
        time.sleep(rand_time*sim_fact)
        print("Motion detected on ",num)
        client.publish(topic,'1',2)
        rand_time, = rng.integers(1, 3, size=1)
        time.sleep(rand_time*sim_fact)
        client.publish(topic,'0',2)

# For Security System Status
def security_alarm(num):
    if fast_simulate:sim_fact=1
    else: sim_fact=10

    rng = np.random.default_rng()
    topic='/{}/sec/alrm{}'.format(group_id,num)
    print(topic)
     
    while(1):
        rand_time, = rng.integers(5, 25, size=1)
        time.sleep(rand_time*sim_fact)
        print("Security alarm on",num)
        client.publish(topic,'1',2)        
        
def door_lock_sensor(num):
    if fast_simulate:sim_fact=1
    else: sim_fact=10

    rng = np.random.default_rng()
    topic='/{}/sec/drlck{}'.format(group_id,num)
    print(topic)

    while(1):
        rand_time, = rng.integers(5, 20, size=1)
        time.sleep(rand_time*sim_fact)
        print(num,"door locked")
        client.publish(topic,'1',2)
        rand_time, = rng.integers(5, 10, size=1)
        time.sleep(rand_time*sim_fact)
        print(num,"door un-locked")
        client.publish(topic,'0',2)

# For Gas sensor
def gas_sensor(num):
    topic='/{}/gas{}'.format(group_id,num)    
    gas=0
    print(topic)

    while(1):    
        if(np.random.randint(1,10*(1-gas)+5*gas)==2):
            gas=int(not gas)
            print("Gas",gas)
            client.publish(topic, gas,2) 
        time.sleep(12-10*int(fast_simulate))

# For Smoke Sensor
def smoke_sensor(num):
    topic='/{}/smk{}'.format(group_id,num)      
    smoke=0
    print(topic)

    while(1):  
        if(np.random.randint(1,10*(1-smoke)+5*smoke)==2):
            smoke=int(not smoke)
            print("Smoke",smoke)
            client.publish(topic, smoke,2)               
        time.sleep(12-10*int(fast_simulate))


client = paho.Client(client_id)
client.username_pw_set(username, password)

print("connecting to broker ", broker)
client.connect(broker)
client.loop_start()  # start loop to process received messages

print('All publishing topics')


# Define Sensors
motion_thr01= Thread(target=motion_sensor, args=('01',))
motion_thr02= Thread(target=motion_sensor, args=('02',))
alarm_thr01=Thread(target=security_alarm,args=('01',))
door_lock_thr01=Thread(target=door_lock_sensor,args=('01',))
door_lock_thr02=Thread(target=door_lock_sensor,args=('02',))

gas_thr01= Thread(target=gas_sensor, args=('01',))
smk_thr01=Thread(target=smoke_sensor,args=('01',))

temp_thr01=Thread(target=periodic_sensor,args=('temp','01',sensor_parameters['temperature-low'],sensor_parameters['temperature-high'],4,30))
hum_thr01=Thread(target=periodic_sensor,args=('hum','02',sensor_parameters['humidity-low'],sensor_parameters['humidity-high'],25,30))
pwr_thr01=Thread(target=periodic_sensor,args=('pwr','03',sensor_parameters['power-consumption-low'],sensor_parameters['power-consumption-high'],150,20))

# Get Sensor readings
motion_thr01.start()
motion_thr02.start()
alarm_thr01.start()
door_lock_thr01.start()
door_lock_thr02.start()

gas_thr01.start()
smk_thr01.start()

temp_thr01.start()
hum_thr01.start()
pwr_thr01.start()

motion_thr01.join() 

client.disconnect() 
