# import the motorcortex library
import motorcortex

# Create a parameter tree object
parameter_tree = motorcortex.ParameterTree()
certificate_path = "mcx.cert.crt" #"~/Documents/Vectioneer/MotorcortexApplication/mcx.cert.crt"

# Open request and subscribe connection
try:
  req, sub = motorcortex.connect(url="wss://192.168.56.101:5568:5567",
                                 motorcortex_types=motorcortex.MessageTypes(), param_tree=parameter_tree,
                                 certificate=certificate_path,
                                 timeout_ms=1000,
                                 login="root", password="secret")
  tree = parameter_tree.getParameterTree()
  print(f"Parameters: {tree}")

  # Requesting the parameter tree
  param_tree_reply = req.getParameterTree()
  param_tree_reply_msg = param_tree_reply.get(0)
  if param_tree_reply_msg:
    print("Parameter tree received")
  else:
    print("Failed to receive parameter tree")
  parameter_tree.load(param_tree_reply_msg)


except RuntimeError as err:
  print(err)
