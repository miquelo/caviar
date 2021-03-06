Secure Shell (SSH)
==================

SSH interfaces.

.. class:: SSHClient

   SSH client.
   
   .. function:: login(target, private_key_path)
   
      Create a session.
      
      :param caviar.network.ssh.SSHUserHost target:
         Remote user target.
      :param str private_key_path:
         Remote user private key path.
         
      :rtype:
         SSHPhysicalSession
      :return:
         The physical SSH session.
         
      :raise caviar.network.ssh.SSHUnavailableSessionError:
         If not any session is available.
         
   .. function:: close()
   
      Close this client.
      
.. class:: SSHPhysicalSession

   SSH physical session.
   
   .. function:: execute(cmd)
   
      Executes a comand
      
      :param str cmd:
         Command to be executed.
         
      :rtype:
         tuple
      :return:
         Tuple of *stdout* and *stderr*.
         
      :raise caviar.network.ssh.SSHInvalidSessionError:
         If the current session is invalid.
         
   .. function:: copy(source_path, target_path):
   
      # TODO ...
      
   .. function:: logout()
   
      Log out.

