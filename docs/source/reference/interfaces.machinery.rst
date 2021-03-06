Machinery
=========

Machinery interfaces.

.. class:: Machinery

   Machinery for GlassFish environment.

   :param dict params:
      Machinery parameters.
   :param str mgmt_public_key_path:
      Management public key path.
   :param fileobj log_out:
      Logging output.
      
   .. function:: server(name, das_public_key_path=None)

      Restore a GlassFish server machine.

      :param str name:
         Name of the machine.
      :param str das_public_key_path:
         Public key path of the DAS machine. It should be `None` if the
         machine to restore is a root DAS itself.

      :rtype:
         ServerMachine
      :return:
         The restored GlassFish server machine.

   .. function:: load_balancer(name, das_public_key_path)

      Restore a GlassFish load balancer machine.

      :param str name:
         Name of the machine.
      :param str das_public_key_path:
         Public key path of the DAS machine.

      :rtype:
         AJP13LoadBalancerMachine
      :return:
         The restored GlassFish load balancer machine.

.. class:: Machine

   Machine for GlassFish environment.
      
   .. py:attribute:: host()
   
      Host of this machine.
      
      :rtype:
         str
         
   .. function:: ping_cmd()
   
      Create a suitable command for ensuring this machine is accessible.
      
      :rtype:
         str
      :return:
         The suitable command.

.. class:: ServerMachine

   Bases: :class:`Machine`

   GlassFish server machine.
   
   .. py:attribute:: node_dir()
   
      System directory of nodes on server machines.
      
      :rtype:
         str
         
   .. py:attribute:: appserver_user()
   
      Application server user name.
      
      :rtype:
         str
      :return:
         The application server user name.
         
   .. py:attribute:: appserver_public_key_path()
   
      Public key file path of application server user.
      
      :rtype:
         str
      :return:
         The public key file path.
         
   .. function:: password_file_path(pwd_id)

      Path relative to `asadmin` command working directory of an already created
      password file identified by the given identifier.

      :param pwd_id:
         The identifier used by this machine to identify the password file.

      :rtype:
         str
      :return:
         The path of the password file.

   .. function:: asadmin_cmd(asadmin_args)

      Create a suitable `asadmin` command for this machine with the given
      arguments.

      :param list asadmin_args:
         `asadmin` utility arguments.

      :rtype:
         str
      :return:
         The suitable command.

   .. function:: create_password_file_cmd(pwd_id, passwords)

      Create a suitable command for creating a password file for `asadmin`
      utility.

      :param pwd_id:
         The identifier used by this machine to identify the password file. It
         should be generated by the caller.
      :param dict passwords:
         A dictionary with `asadmin` known key passwords.

      :rtype:
         str
      :return:
         The suitable command.

   .. function:: delete_password_file_cmd(pwd_id)

      Create a suitable command for deleting a previous created password file.

      :param pwd_id:
         The identifier used by this machine to identify the password file.
         
      :rtype:
         str
      :return:
         The suitable command.

   .. function:: install_master_password_cmd(domain_name, node_name, node_host)

      Create a suitable command for copying the saved master password of the
      domain with the given name to the specified node with the given name and
      host.

      :param str domain_name:
         Name of the source domain.
      :param str node_name:
         Name of the target node.
      :param str node_host:
         Host of the target node.

      :rtype:
         str
      :return:
         The suitable command.
            
   .. function:: keytool_put_begin_cmd(domain_name)
   
      # TODO ...
      
   .. function:: keytool_put_end_cmd(domain_name, alias, master_password, \
      file_path)
   
      # TODO ...
      
   .. function:: keytool_certificate_path(domain_name)
   
      # TODO ...
      
   .. function:: keytool_key_path(domain_name)
   
      # TODO ...
      
.. class:: AJP13LoadBalancerMachine

   Bases: :class:`Machine`

   AJP/1.3 load balancer machine.
   
   .. py:attribute:: web_user()
   
      Web user name.
      
      :rtype:
         str
         
   .. function:: add_instance_cmd(name, host, port)

      Create a suitable command for adding an instance to this load balancer.

      :param str name:
         Instance name.
      :param str host:
         Instance host.
      :param str port:
         Instance port.

      :rtype:
         str
      :return:
         The suitable command.

   .. function:: remove_instance_cmd(name)

      Create a suitable command for removing an instance from this load
      balancer.

      :param str name:
         Instance name.

      :rtype:
         str
      :return:
         The suitable command.
