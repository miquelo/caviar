TODO
====

* ¿El certificado del LB debe estar en el DAS? A tener en cuenta, el keystore
  del DAS se copia en la creación de la instancia. Efectos esperados:
  - Certificado de administración (DAS e instancias)
  - Certificado de conexión segura entre LB e instancias (DAS e instancias)
  - Certificado de LB (LB)
  
  https://docs.oracle.com/cd/E18930_01/html/821-2416/gfaad.html#gjpan
  https://serverfault.com/questions/390529/ssl-certificate-install-glassfish-or-apache-or-both

* Por cada dominio de DAS, pueden haver múltiples dominios de LB

* Nuevas interfaces (Módulo 'certificate'):
  - CertificateKey
    + certificate: Certificate
    + key: PrivateKey
  - Certificate
    + open(): fileobj
  - PrivateKey
    + password: str
    + open(): fileobj
    
* Implementaciones:
  - caviar.certificate.CertificateKey(CertificateKey)
  - caviar.certificate.file.FileCertificate(Certificate)
  - caviar.certificate.file.FilePrivateKey(PrivateKey)

