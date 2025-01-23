# import the motorcortex library
import motorcortex
# Create a parameter tree object
parameter_tree = motorcortex.ParameterTree()
# Open request and subscribe connection
try:
  req, sub = motorcortex.connect("wss://192.168.56.101:5568:5567", motorcortex.MessageTypes(), parameter_tree,
                                   certificate="mcx.cert.crt", timeout_ms=1000,
                                   login="root", password="secret")
  tree = parameter_tree.getParameterTree()
  print(f"Parameters: {tree}")

except RuntimeError as err:
    print(err)
