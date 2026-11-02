# Manual de Producto — NovaTech CloudSuite

Versión 2.5 — Actualizado octubre 2026

## 1. ¿Qué es NovaTech CloudSuite?

NovaTech CloudSuite es una plataforma SaaS de gestión documental con capacidades de inteligencia artificial, orientada a empresas medianas y grandes del sector financiero, salud y manufactura. La plataforma centraliza la administración de documentos corporativos y permite realizar búsquedas semánticas, extracción automática de datos y clasificación inteligente.

## 2. Planes disponibles

NovaTech CloudSuite ofrece tres planes comerciales:

### 2.1 Plan Starter

Dirigido a equipos pequeños de hasta 25 usuarios. Incluye almacenamiento de hasta 500 GB, hasta 10.000 documentos procesados por mes y acceso al módulo de búsqueda semántica básica. El precio es de 199 USD mensuales por organización.

### 2.2 Plan Business

Dirigido a empresas medianas de 26 a 250 usuarios. Incluye almacenamiento de hasta 5 TB, hasta 100.000 documentos procesados por mes, módulo de búsqueda semántica avanzada, extracción automática de campos y clasificación inteligente. El precio es de 799 USD mensuales por organización.

### 2.3 Plan Enterprise

Dirigido a organizaciones de más de 250 usuarios. Incluye almacenamiento ilimitado, procesamiento ilimitado de documentos, todas las capacidades del Plan Business, integración con sistemas corporativos (SAP, Salesforce, Oracle), SLA del 99.9% y gestor de cuenta dedicado. El precio es personalizado según los requerimientos del cliente.

## 3. Formatos soportados

NovaTech CloudSuite soporta los siguientes formatos de documento para ingesta y procesamiento:

- Documentos de texto: PDF, DOCX, DOC, TXT, RTF, ODT.
- Hojas de cálculo: XLSX, XLS, CSV.
- Presentaciones: PPTX, PPT.
- Imágenes con OCR: JPG, PNG, TIFF.

El tamaño máximo por documento es de 100 MB en los planes Starter y Business, y 500 MB en el plan Enterprise.

## 4. Arquitectura técnica

La plataforma está desplegada en AWS, utilizando los siguientes servicios principales:

- Amazon S3 para almacenamiento primario de documentos.
- Amazon OpenSearch para indexación textual y búsqueda semántica.
- Amazon Bedrock para los modelos de inteligencia artificial.
- Amazon RDS Aurora PostgreSQL para la base de datos relacional.
- Amazon ECS Fargate para los microservicios de aplicación.

Toda la información en tránsito y en reposo está cifrada con AES-256. Los documentos pueden opcionalmente cifrarse con claves gestionadas por el cliente a través de AWS KMS en el plan Enterprise.

## 5. Integraciones disponibles

La plataforma ofrece integraciones nativas con:

- Microsoft 365 (SharePoint, OneDrive, Outlook).
- Google Workspace (Drive, Gmail).
- Slack para notificaciones.
- Microsoft Teams para notificaciones.
- Zapier para automatizaciones personalizadas.

Las integraciones con SAP, Salesforce y Oracle requieren el plan Enterprise y se habilitan mediante conectores dedicados.

## 6. SLA y disponibilidad

NovaTech CloudSuite garantiza los siguientes niveles de servicio:

- Plan Starter: 99.0% de disponibilidad mensual.
- Plan Business: 99.5% de disponibilidad mensual.
- Plan Enterprise: 99.9% de disponibilidad mensual.

En caso de incumplimiento del SLA, el cliente recibe créditos aplicables a futuras facturaciones según la tabla definida en el contrato comercial.

## 7. Soporte

El soporte técnico se ofrece a través de los siguientes canales:

- Plan Starter: soporte por correo electrónico, respuesta en máximo 48 horas hábiles.
- Plan Business: soporte por correo y chat, respuesta en máximo 8 horas hábiles.
- Plan Enterprise: soporte 24/7 por correo, chat y teléfono, con tiempos de respuesta diferenciados según severidad.
