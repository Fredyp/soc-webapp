# SOC WebApp

Una aplicación web ligera desarrollada en Flask para equipos SOC. Permite:

- Crear cuentas de clientes con su correo electrónico.
- Generar y enviar informes en PDF por correo.
- Registrar y visualizar envíos anteriores en un historial por cliente.

## 🚀 Instalación rápida en Ubuntu

```bash
curl -s https://raw.githubusercontent.com/tuusuario/soc-webapp/main/install_and_run.sh | bash
```

## 🧱 Estructura del proyecto

```
soc_webapp/
├── app.py
├── requirements.txt
├── install_and_run.sh
├── templates/
│   ├── index.html
│   ├── create_report.html
│   ├── report_log.html
│   └── report_template.html
└── .gitignore
```

## 📤 Envío de informes

Los informes se generan desde formularios HTML, se convierten a PDF usando `pdfkit` y se envían por correo usando `Flask-Mail`.

## 📄 Licencia

MIT - Libre uso y modificación.