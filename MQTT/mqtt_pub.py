import mqtt_client
import sys

if '-p' in sys.argv:
    index_p= sys.argv.index('-p')
    puerto= int(sys.argv[index_p+1]) 
else: 
    puerto=1883

if '-t' in sys.argv:
    index_t= sys.argv.index('-t')
    topico= sys.argv[index_t+1]
else:
    print('A topic must be provided')
    sys.exit()

if '-c' in sys.argv:
    index_id= sys.argv.index('-c')
    id= sys.argv[index_id+1]
else:
    id= 'client_pub'

if '-m' in sys.argv:
    index_m= sys.argv.index('-m')
    mensaje= sys.argv[index_m+1]
else:
    print('A message must be provided')
    sys.exit()

print(id)

cl = mqtt_client.Publisher()
cl.set_connect_packet(id)
cl.connect(port=puerto)
cl.set_publish_packet(topico,mensaje)
cl.publish()
cl.disconnect()
