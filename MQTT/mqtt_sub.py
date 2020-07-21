import mqtt_client
import sys

if '-c' in sys.argv:
    index_id= sys.argv.index('-c')
    id= sys.argv[index_id+1]
else:
    id= 'client_sub'

if '-p' in sys.argv:
    index_p= sys.argv.index('-p')
    puerto= int(sys.argv[index_p+1])
else:
    puerto= 1883

if '-t' in sys.argv:
    index_t= sys.argv.index('-t')
    topico= sys.argv[index_t+1]
else:
    print('A topic must be provided')
    sys.exit()


cl = mqtt_client.Subscriber()
cl.set_connect_packet(id)
cl.connect(port=puerto)
cl.set_subscribe_packquet(topico)
cl.subscribe()