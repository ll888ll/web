from __future__ import annotations

import importlib.util
from pathlib import Path
from shutil import copy2

from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command


class Command(BaseCommand):
    help = 'Ejecuta el servidor de desarrollo con HTTPS usando django-sslserver.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--address',
            default='127.0.0.1:8443',
            help='Host y puerto para HTTPS (por defecto: 127.0.0.1:8443).',
        )
        parser.add_argument(
            '--cert',
            default=None,
            help='Ruta al certificado a usar (por defecto ssl/dev.crt).',
        )
        parser.add_argument(
            '--key',
            default=None,
            help='Ruta a la clave privada (por defecto ssl/dev.key).',
        )

    def handle(self, *args, **options):
        have_sslserver = bool(importlib.util.find_spec('sslserver'))
        if not have_sslserver:
            self.stdout.write(
                self.style.WARNING(
                    'django-sslserver no está instalado. Ejecutando en HTTP con runserver como fallback.'
                )
            )
            # Permite usar el mismo --address para runserver (p.ej. 127.0.0.1:8443)
            address = options['address']
            self.stdout.write(self.style.SUCCESS(f'Servidor HTTP listo en http://{address}/'))
            call_command('runserver', address)
            return

        # HTTPS dev con sslserver
        self._monkeypatch_ssl_wrap_socket()

        cert_path = self._resolve_path(options['cert'], 'dev.crt')
        key_path = self._resolve_path(options['key'], 'dev.key')

        if not cert_path.exists() or not key_path.exists():
            if options['cert'] or options['key']:
                raise CommandError(
                    f'No se encontraron los archivos provistos ({cert_path} / {key_path}). '
                    'Crea tu propio certificado o deja los parámetros por defecto.'
                )
            self._ensure_dev_cert(cert_path, key_path)

        address = options['address']
        self.stdout.write(
            self.style.SUCCESS(
                f'Servidor HTTPS listo en https://{address}/ (certificado: {cert_path}, clave: {key_path})'
            )
        )
        call_command(
            'runsslserver',
            address,
            certificate=str(cert_path),
            key=str(key_path),
        )

    def _resolve_path(self, provided: str | None, default_name: str) -> Path:
        if provided:
            return Path(provided).expanduser().resolve()
        ssl_dir = Path(settings.BASE_DIR) / 'ssl'
        ssl_dir.mkdir(parents=True, exist_ok=True)
        return ssl_dir / default_name

    def _ensure_dev_cert(self, cert_path: Path, key_path: Path) -> None:
        from sslserver.management.commands.runsslserver import default_ssl_files_dir

        default_dir = Path(default_ssl_files_dir())
        default_cert = default_dir / 'development.crt'
        default_key = default_dir / 'development.key'

        if not default_cert.exists() or not default_key.exists():
            raise CommandError(
                'django-sslserver no trae certificados de desarrollo. '
                'Genera un certificado manualmente y pásalo con --cert/--key.'
            )

        copy2(default_cert, cert_path)
        copy2(default_key, key_path)
        self.stdout.write(
            self.style.WARNING(
                f'Copiando certificado de ejemplo de django-sslserver a {cert_path} / {key_path}.'
            )
        )

    def _monkeypatch_ssl_wrap_socket(self) -> None:
        import ssl

        if hasattr(ssl, 'wrap_socket'):
            return

        def _wrap_socket(socket, keyfile=None, certfile=None, server_side=False,
                         cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLS,
                         ca_certs=None, do_handshake_on_connect=True,
                         suppress_ragged_eofs=True, server_hostname=None,
                         session=None):
            context = ssl.SSLContext(ssl_version)
            context.check_hostname = False
            context.verify_mode = cert_reqs
            if certfile:
                context.load_cert_chain(certfile, keyfile)
            if ca_certs:
                context.load_verify_locations(cafile=ca_certs)
            return context.wrap_socket(
                socket,
                server_side=server_side,
                do_handshake_on_connect=do_handshake_on_connect,
                suppress_ragged_eofs=suppress_ragged_eofs,
                server_hostname=server_hostname,
                session=session,
            )

        ssl.wrap_socket = _wrap_socket  # type: ignore[attr-defined]
