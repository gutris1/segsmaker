import subprocess
import threading
import sys
import os

os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def zrok_launch(token, launch_args):
    
    subprocess.run(
        f"mkdir -p /tmp/models /tmp/Lora /tmp/ControlNet",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    
    try:
        zrok_process = subprocess.Popen(['python', 'zrok.py', token], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        launch_process = subprocess.Popen(['python', 'launch.py'] + launch_args,
                                           stdout=sys.stdout, stderr=sys.stdout, text=True)

        def capture_output(process):
            try:
                if process.stdout is not None:
                    for line in process.stdout:
                        print(line.strip())
                        
            except Exception:
                pass

        zrok_thread = threading.Thread(target=capture_output, args=(zrok_process,))
        launch_thread = threading.Thread(target=capture_output, args=(launch_process,))

        zrok_thread.start()
        launch_thread.start()

        zrok_thread.join()
        launch_thread.join()

    except KeyboardInterrupt:
        pass
    
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    token = sys.argv[1]
    launch_args = sys.argv[2:]
    zrok_launch(token, launch_args)
