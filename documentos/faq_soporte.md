# FAQ de Soporte Técnico — NovaTech CloudSuite

Última actualización: octubre 2026

## Cuentas y acceso

### ¿Cómo recupero mi contraseña?

Para recuperar la contraseña, ingresa a la URL de login de tu organización y haz clic en "¿Olvidaste tu contraseña?". El sistema enviará un enlace de restablecimiento al correo electrónico asociado a tu cuenta. El enlace tiene una vigencia de 60 minutos.

Si no recibes el correo en 10 minutos, revisa tu carpeta de spam. Si persiste el problema, contacta a tu administrador de cuenta o al equipo de soporte.

### ¿Cómo activo la autenticación multifactor?

Dentro de la plataforma, ve a tu perfil de usuario, selecciona "Seguridad" y luego "Activar MFA". El sistema te permitirá vincular una aplicación de autenticación como Google Authenticator, Microsoft Authenticator o Authy. Escanea el código QR y guarda los códigos de respaldo en un lugar seguro.

A partir de enero de 2027 la autenticación multifactor será obligatoria para todos los planes.

### ¿Puedo iniciar sesión con mi cuenta corporativa (SSO)?

Sí. Los planes Business y Enterprise soportan Single Sign-On a través de SAML 2.0 y OpenID Connect. La configuración de SSO la debe realizar el administrador de la cuenta siguiendo la guía disponible en el centro de ayuda. Los proveedores de identidad compatibles incluyen Microsoft Entra ID, Okta, Google Workspace y OneLogin.

## Carga y procesamiento de documentos

### ¿Por qué un documento se queda en estado "Procesando"?

El procesamiento de un documento puede tardar entre 30 segundos y 5 minutos dependiendo del tamaño y la complejidad. Si un documento permanece en estado "Procesando" por más de 15 minutos, generalmente se debe a una de estas causas:

- El documento está corrupto o parcialmente dañado.
- El formato del documento no es compatible.
- El OCR falló por una calidad muy baja de la imagen.
- El cupo mensual del plan fue superado.

Para resolverlo, intenta eliminar el documento y volverlo a subir. Si persiste, abre un ticket adjuntando el ID del documento.

### ¿Puedo subir documentos por lotes?

Sí. La plataforma permite subida de hasta 100 documentos simultáneos por sesión en el Plan Business y hasta 1.000 documentos simultáneos en el Plan Enterprise. También puedes usar la API REST para automatizar cargas masivas desde tus sistemas.

### ¿Qué pasa con los documentos cuando elimino mi cuenta?

Al eliminar una cuenta, los documentos permanecen disponibles durante 30 días en estado de "retención" para posibles recuperaciones. Después de ese periodo, se eliminan permanentemente de todos los sistemas, incluyendo backups. Este proceso cumple con los lineamientos del Reglamento General de Protección de Datos (GDPR) y la Ley 1581 de Protección de Datos Personales de Colombia.

## Facturación

### ¿Cuáles son los medios de pago aceptados?

Aceptamos tarjetas de crédito Visa, Mastercard y American Express para los planes Starter y Business. Para el plan Enterprise, aceptamos adicionalmente transferencia bancaria y pago por factura con términos de 30 días.

### ¿Puedo cambiar de plan en cualquier momento?

Sí. Los cambios de plan superior (upgrade) son inmediatos y se prorratean en la facturación del siguiente mes. Los cambios a plan inferior (downgrade) se aplican al inicio del siguiente ciclo de facturación.

## Problemas comunes

### El OCR no está reconociendo bien el texto de mi documento escaneado

El OCR funciona óptimamente con documentos escaneados a 300 DPI o superior. Si estás obteniendo baja precisión, verifica que el documento no esté torcido, que tenga buen contraste y que el texto esté enfocado. En casos de documentos de muy baja calidad, considera reescanear el documento antes de volver a subirlo.

### No puedo acceder a un documento compartido conmigo

Verifica que estés autenticado con la cuenta correcta. Si el documento fue compartido con una cuenta diferente, pide al propietario que te lo comparta nuevamente con la cuenta correcta. También revisa que el enlace no haya expirado.

## Contacto con soporte

Para contactar al equipo de soporte, puedes usar los siguientes canales según tu plan:

- Correo electrónico: soporte@novatechcloudsuite.com (todos los planes).
- Chat en la plataforma: planes Business y Enterprise.
- Teléfono: +57 601 555 0100 (solo plan Enterprise).

El horario de atención por chat y teléfono es de lunes a viernes de 7:00 a. m. a 7:00 p. m. hora de Colombia (UTC-5). El soporte 24/7 del plan Enterprise opera por correo electrónico fuera de este horario.
