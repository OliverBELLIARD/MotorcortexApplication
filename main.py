# import the motorcortex library
import motorcortex
import time


parameter_tree = motorcortex.ParameterTree()
certificate_path = "mcx.cert.crt" #"~/Documents/Vectioneer/MotorcortexApplication/mcx.cert.crt"

# Define the callback function that will be called whenever a message is received
def message_received(parameters):
  for cnt in range(0, len(parameters)):
    param = parameters[cnt]
    timestamp = param.timestamp.sec + param.timestamp.nsec * 1e-9
    value = param.value
    # print the timestamp and value; convert the value to a string first
    # so we do not need to check all types before printing it
    print(f"Notify: {timestamp}, {value}")


def main():
  # Create a parameter tree object
  parameter_tree = motorcortex.ParameterTree()
  # Open request and subscribe connection
  try:
    req, sub = motorcortex.connect(url="wss://192.168.56.101:5568:5567",
                              motorcortex_types=motorcortex.MessageTypes(), param_tree=parameter_tree,
                              certificate=certificate_path,
                              timeout_ms=1000,
                              login="root", password="secret")
    tree = parameter_tree.getParameterTree()
    print(f"Parameters: {tree}")

  except RuntimeError as err:
    print(err)
    exit()

  paths = ['root/Control/hostInJointVelocity']
  # define the frequency divider that tells the server to publish only every
  # n-th sample. This depends on the update rate of the publisher.
  divider = 100
  # subscribe and wait for the reply with a timeout of 10 seconds
  subscription = sub.subscribe(paths, 'group1', divider)
  # get reply from the server
  is_subscribed = subscription.get()
  # print subscription status and layout
  if (is_subscribed is not None) and (is_subscribed.status == motorcortex.OK):
    print(f"Subscription successful, layout: {subscription.layout()}")
  else:
    print(f"Subscription failed, do your paths exist? \npaths: {paths}")
    sub.close()
    exit()
    
  # set the callback function that handles the received data
  # Note that this is a non-blocking call, starting a new thread that handles
  # the messages. You should keep the application alive for a s long as you need to
  # receive the messages
  subscription.notify(message_received)
  
  # polling subscription
  for i in range(100):
    value = subscription.read()
    if value:
      print(f"Polling, timestamp: {value[0].timestamp} value: {value[0].value}")
    time.sleep(1)

  # close the subscription when done
  sub.close()
  # Close connection for a fresh restart
  req.close()

if __name__ == "__main__":
  main()