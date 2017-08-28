Certificate
===========

Certificate interfaces.

.. class:: CertificateKey

   Pair of certificate and private key.
   
   .. py:attribute:: certificate()
   
      Certificate element.
      
      :rtype:
         Certificate
         
   .. py:attribute:: key()
   
      Private key element.
      
      :rtype:
         PrivateKey
         
.. class:: Certificate

   Certificate object.
   
   .. function:: open()
   
      Open this certificate for reading it.
      
      :rtype:
         fileobj
      :return:
         A file object for reading this certificate.
         
.. class:: PrivateKey

   Private key object.
   
   .. py:attribute:: password()
   
      Password used for encrypting this private key, if any.
      
      :rtype:
         str
         
   .. function:: open()
   
      Open this private key for reading it.
      
      :rtype:
         fileobj
      :return:
         A file object for reading this private key.
         

