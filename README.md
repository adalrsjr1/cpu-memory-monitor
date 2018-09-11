## Usage

`python3 monitor.py <memory_notation> <pid_file>`
where memory_notation:
  k = kilobytes
  m = megabytes
  g = gigabytes
  otherwise = bytes

## Self-saving PID in Java 8 or before

```
int savePid(String filepath) {
		int pid = Integer.parseInt(new File("/proc/self").getCanonicalFile().getName())
		File tmp = new File(filepath)
		tmp.write(pid)
		return pid
}
```
