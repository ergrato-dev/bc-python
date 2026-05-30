# Recursos — Semana 26: Cloud Storage y Assets

## Webgrafía

### Documentación oficial

| Recurso | URL | Por qué vale la pena |
|---------|-----|----------------------|
| boto3 S3 Docs | https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html | Referencia completa de métodos S3 |
| AWS S3 User Guide | https://docs.aws.amazon.com/AmazonS3/latest/userguide/ | Conceptos, seguridad, lifecycle |
| Google Drive API v3 | https://developers.google.com/drive/api/reference/rest/v3 | Referencia REST completa |
| google-api-python-client | https://googleapis.github.io/google-api-python-client/docs/ | Guía del cliente Python |
| google-auth Docs | https://google-auth.readthedocs.io/ | Service Account, OAuth2 flows |

### Guías prácticas

| Recurso | Tema |
|---------|------|
| [AWS — Uploading objects using multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) | Cuándo y cómo usar multipart |
| [AWS — Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) | Seguridad y expiración |
| [AWS — S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/) | Comparativa de costos y latencia |
| [AWS — Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) | Automatizar transiciones |
| [Google — Service Account Auth](https://cloud.google.com/docs/authentication/provide-credentials-adc) | ADC y Service Accounts |
| [Google — Drive: Manage Uploads](https://developers.google.com/drive/api/guides/manage-uploads) | Resumable, multipart |

---

## Stack técnico de la semana

```
boto3                      # cliente AWS — S3, IAM, y 200+ servicios
boto3-stubs[s3]            # type stubs para mypy strict
google-api-python-client   # cliente REST Google APIs
google-auth                # OAuth2 / Service Account
pydantic-settings          # configuración desde .env / variables de entorno
```

### Instalación rápida

```bash
pip install boto3 boto3-stubs[s3] google-api-python-client google-auth pydantic-settings
```

---

## Herramientas complementarias

| Herramienta | Uso |
|-------------|-----|
| [LocalStack](https://localstack.cloud/) | Emulación local de servicios AWS (S3, SQS, etc.) |
| [AWS CLI](https://docs.aws.amazon.com/cli/latest/) | `aws s3 ls`, `aws s3 cp` — debug rápido |
| [S3 Browser](https://s3browser.com/) | GUI para explorar buckets S3 en Windows |
| [Cyberduck](https://cyberduck.io/) | GUI multi-cloud (S3, Drive, SFTP) |
| [rclone](https://rclone.org/) | Sync CLI para +40 providers cloud |

---

## Testing sin credenciales reales

```bash
# Iniciar LocalStack (emula S3 localmente)
docker run -p 4566:4566 localstack/localstack

# Apuntar boto3 a LocalStack
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
```

---

## Navegación

← [Teoría](../1-teoria/) · [Proyecto](../3-proyecto/)
