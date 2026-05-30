# Sitios Web — Semana 26: Cloud Storage y Assets

## Amazon S3 y boto3

| Recurso | Descripción |
|---------|-------------|
| [boto3 S3 API Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) | Referencia completa de todos los métodos del cliente S3 |
| [AWS S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/) | Guía oficial: conceptos, seguridad, lifecycle, replicación |
| [AWS — Multipart Upload Overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) | Cuándo y cómo usar multipart upload para archivos grandes |
| [AWS — Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) | Seguridad, expiración, casos de uso de URLs firmadas |
| [AWS — S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/) | Comparativa de costos, latencia y casos de uso por clase |
| [AWS — Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) | Automatizar transiciones entre storage classes |
| [AWS — S3 Transfer Acceleration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html) | Uploads más rápidos desde ubicaciones remotas vía CloudFront |

## Google Drive API

| Recurso | Descripción |
|---------|-------------|
| [Google Drive API v3 Reference](https://developers.google.com/drive/api/reference/rest/v3) | Referencia REST completa: Files, Permissions, Drives |
| [google-api-python-client Docs](https://googleapis.github.io/google-api-python-client/docs/) | Guía del cliente Python oficial de Google APIs |
| [google-auth Docs](https://google-auth.readthedocs.io/) | Service Account, OAuth2 flows, Application Default Credentials |
| [Google — Service Account Auth](https://cloud.google.com/docs/authentication/provide-credentials-adc) | Cómo configurar ADC y Service Accounts |
| [Google — Drive: Manage Uploads](https://developers.google.com/drive/api/guides/manage-uploads) | Resumable upload, multipart upload, chunking |
| [Google — Drive: Manage Sharing](https://developers.google.com/drive/api/guides/manage-sharing) | Permisos, roles, dominios, link sharing |

## Testing y Herramientas

| Recurso | Descripción |
|---------|-------------|
| [LocalStack Docs](https://docs.localstack.cloud/) | Emulación local de AWS (S3, SQS, Lambda) para tests sin costo |
| [moto — Mock AWS Services](https://docs.getmoto.org/en/latest/) | Librería Python para mockear servicios AWS en tests |
| [AWS CLI S3 Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/) | `aws s3 ls`, `aws s3 cp`, `aws s3 sync` — debugging rápido |
| [rclone Documentation](https://rclone.org/docs/) | Sync CLI para 40+ providers: S3, Drive, GCS, Backblaze B2 |

## Conceptos Complementarios

| Recurso | Descripción |
|---------|-------------|
| [AWS — IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) | Least privilege, roles vs. access keys, MFA |
| [AWS — S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html) | Block Public Access, cifrado, logging, políticas de bucket |
| [Google Cloud — Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-service-accounts) | Cómo limitar permisos y rotar credenciales |
