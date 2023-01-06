Ayberk Toptan

Simple Secure Bank Server with Multiple Clients

Python was used as programming language
For performing encryption and decryption the RSA is used.
	However, because rsa is not default library in pyhton,
	in order to make it importable and usable in the script
	it must be installed by running the code 'pip install rsa' in terminal
	if it has not been installed already.
How to execute:
	server execution: python3 server.py <server_port>
        example: python3 server.py 3405
        (if you are in the same directory with server.py)
    client execution: python3 client.py <server_domain> <server_port>
        <server_domain> is which domain the server is running
        ex: python3 client.py localhost
        (if you are in the same directory with client.py)
    
    (port numbers must match)

	Additional explanations:
	
	I seperated the the client and server side with their own directories.
	In the main directory I have a script called 'preExecute.py' which creates
	public and private keys and puts them to the server directory and puts
	the same public key to the client directory to use them for encryption
	and decryption. Also, it creates the needed files which are balance and
	passwd with default users and balances given in the instruction pdf, and
	it puts these files into the server directory because they will be using
	by server. The script has already been executed, so needed files and
	keys were created, and my submission includes them. Therefore no needed
	to execute again this script but in any case you now know how to execute it.
	To execute 'preExecute.py', you need to be inside of the main directory,
	not in client or server directory.
	As it is asked to build the server accepts one client and once the client
	exits it accepts onother client which means keeps listening. My server
	does this, in addition, I used threads so my server also can accept multiple
	clients at the same time and process their actions.
	Finally, once the client chooses the action '2' which is 'exit',
	my server updates the balance file with the latest balances.
	To increase performs by not opening file and writing after each action
	like deposit I choosed to write latest values once the client exits.
	TO do so, once my server started to run, it opens the files balance and
	passwd, and puts the data seperatly in dictionaries called balances and users.
	Then, for instance after each deposit, it updates the logged in client's
	balance in the balances dictionary. Once the client exits, it writes latest
	balances inside of balances dictionary to the 'balance' file.
	For hashing passwords, I used MD5, it is already in the python library of
	hashlib. Once I hashed the passwords with MD5 function of hashlib, I saved
	them in the 'passwd' file by taking their hexdigest values 
	by calling hexdigist function.