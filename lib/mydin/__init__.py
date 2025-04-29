

def configure( ControlerClass, BackplaneClass ):
	din = ControlerClass( BackplaneClass )
	# Ask backplane to expose its properties on the contoler
	din.backplane.attach( din )
	return din