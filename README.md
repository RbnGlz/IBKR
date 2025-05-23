# Verificador de Conexión a Interactive Brokers

Este script permite verificar rápidamente la conexión a la API de Interactive Brokers (IB), mostrando solo mensajes relevantes y ocultando errores no esenciales.

## Requisitos

- Python 3.6 o superior
- Biblioteca `ibapi` de Interactive Brokers
- TWS (Trader Workstation) o IB Gateway en ejecución

## Instalación

1. Clone o descargue este repositorio
2. Instale las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

Asegúrese de que TWS o IB Gateway esté en ejecución antes de ejecutar el script.

```bash
python ib_connection_checker.py
```

### Opciones disponibles

- `--host`: Dirección IP del TWS o IB Gateway (por defecto: 127.0.0.1)
- `--port`: Puerto de conexión (por defecto: 7497 para TWS demo)
  - 7497: TWS demo
  - 7496: TWS real
  - 4002: IB Gateway demo
  - 4001: IB Gateway real
- `--client-id`: ID de cliente (por defecto: 1)
- `--timeout`: Tiempo máximo de espera en segundos (por defecto: 10)

### Ejemplo

```bash
python ib_connection_checker.py --port 4001 --client-id 123
```

## Interpretación de resultados

- ✅ Conexión exitosa: El script se conectó correctamente a la API de IB
- ❌ Error: Se muestra un mensaje de error específico y relevante

El script también devuelve un código de salida:
- 0: Conexión exitosa
- 1: Error de conexión

## Notas importantes

- Asegúrese de habilitar las conexiones API en TWS o IB Gateway
- Configure correctamente el puerto según su entorno (demo o real)
- Utilice un ID de cliente único si tiene múltiples aplicaciones conectadas
