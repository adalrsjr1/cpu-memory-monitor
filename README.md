Realtime CPU and memory monitor to measure and visualise resources
consumption in homemade projects. This is a simple project inspired by
a question from stackoverflow:
https://stackoverflow.com/questions/41133281/better-way-to-implement-matplotlib-animation-with-live-data-from-cpu

## How to run

1. Make sure that you have Python and virtualenv installed
2. Run virtualenv into project's folder and use `pip` to install `requirements.txt`
3. `pip install -r requirements`
4. Run the script as depicted below.

## Usage

`python monitor.py <memory_notation> <pid_file>`

where memory_notation:

  k = kilobytes

  m = megabytes

  g = gigabytes

  otherwise = bytes

## Example for self-saving PID in Java 8 or before

```
// this snippet was tested only on Linux
int savePid(String filepath) {
  int pid = Integer.parseInt(new File("/proc/self").getCanonicalFile().getName());
  File tmp = new File(filepath);
  tmp.write(pid);
  return pid;
}
```
