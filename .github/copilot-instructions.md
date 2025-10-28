Project: Mock Sensor Simulator (asyncio + serial simulation)

Goal
 - Help AI agents make small, safe code changes: add sensors, fix I/O, improve logging, or update async flows.

Quick architecture summary
 - Entrypoint: `SerialApp.py` creates components and runs the asyncio event loop.
 - Components:
   - `Sensor` (in `Sensor.py`): single sensor generator producing strings like "TEMP,12.34,C".
   - `SensorManager` (in `SensorManager.py`): holds sensors and emits combined lines via `generate_all_data()`.
   - `SerialWriter` (in `SerialWriter.py`): opens a serial write connection and periodically writes `Message,{data_line}`.
   - `SerialReader` (in `SerialReader.py`): listens on a serial port, prints received lines and appends them to `serial_output.txt`.
   - `KeyPressHandler` (in `KeyPressHandler.py`): uses `msvcrt` to detect 'q' to set a stop event.

Important patterns & conventions
 - Asyncio-first: long-running I/O is implemented with async def + asyncio.Event for graceful shutdown. Tasks are created with `asyncio.create_task(...)` and cancelled on stop.
 - Serial I/O uses `serial_asyncio.open_serial_connection(url=..., baudrate=...)` returning (reader, writer) pair.
 - Files use synchronous-looking helpers but rely on async libs: use `aiofiles` for async file writes (as `SerialReader` does).
 - Stop signaling: components accept a shared `asyncio.Event` (named `stop_event`) and should periodically check `stop_event.is_set()` and return/cleanup when set.

Run / debug notes (Windows)
 - The project expects serial ports (example: `COM10` write, `COM11` read). For local testing use a virtual serial port pair (com0com or similar).
 - Typical run: `python SerialApp.py` (it constructs `SerialApp(read_port="COM11", write_port="COM10")` when run as __main__).
 - Keyboard stop: press `q` or Ctrl+C. `KeyPressHandler` uses `msvcrt` so it runs only on Windows.

Code conventions & small antipatterns to watch for
 - Hard-coded ports in `SerialApp.py` and in the file-level `if __name__ == "__main__"` blocks: prefer dependency injection/CLI args for changes.
 - SensorManager.generate_all_data() returns a string already terminated with a newline. `SerialWriter` adds another `\n` when composing messages; be careful to avoid double newlines.
 - Some files include commented-out example mains; use them for local unit-style experimentation but prefer `SerialApp.py` as the canonical orchestrator.
 - Type hints present but minimal. Keep signature patterns consistent: async methods take `stop_event: asyncio.Event`.

Integration points & dependencies
 - External libraries: `serial_asyncio`, `aiofiles` (see `Requirements.txt`).
 - OS-specific: `msvcrt` (Windows only) for keypress detection.
 - Output log: `serial_output.txt` is appended by `SerialReader`.

Examples for common change requests
 - Add a sensor: modify `SerialApp.__init__` or call `sensor_manager.add_sensors(Sensor("NAME", min, max, "unit"))`. Example: `Sensor("CO2", 300, 800, "ppm")`.
 - Change write interval: update `SerialWriter(interval=...)` in `SerialApp` constructor; the writer loop uses `asyncio.sleep(0.1)` currently—search for `await asyncio.sleep` to adjust behavior.
 - Improve shutdown: ensure any new component accepts the shared `stop_event`, checks it frequently, and closes serial writer with `writer.close()` and `await writer.wait_closed()`.

What NOT to change without testing
 - Replace `msvcrt` with cross-platform input handling unless adding platform guards; tests/use on Windows expected.
 - Serial framing: don't change the `Message,{data_line}` framing without updating both writer and any consumers.

Files to inspect for PRs
 - `SerialApp.py`, `SerialWriter.py`, `SerialReader.py`, `Sensor.py`, `SensorManager.py`, `KeyPressHandler.py`, `README.md`, `Requirements.txt`.

If something is unclear ask for
 - Which serial port or virtual port pair to use for testing locally.
 - Whether message framing should be changed (e.g., JSON vs CSV).

Short checklist for a safe PR
 - Update/add unit or manual test demonstrating change (small script or commented main is acceptable).
 - Keep async shutdown pattern: accept `stop_event`, check frequently, close serial handles.
 - Run `python SerialApp.py` on Windows with virtual ports to smoke-test.
