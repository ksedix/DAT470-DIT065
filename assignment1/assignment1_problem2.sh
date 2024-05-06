echo This script is being run by `whoami`

cpu_model=$(grep "model name" /proc/cpuinfo | sort -u | cut -d ":" -f2 | awk '{$1=$1} END {print}')
number_of_cpus=$(lscpu | grep "Socket(s)" | cut -d ":" -f2 | tr -d " ")
number_of_cores=$(lscpu | grep "Core(s) per socket" | cut -d ":" -f2 | tr -d " ")
number_of_threads=$(lscpu | grep "Thread(s) per core" | cut -d ":" -f2 | tr -d " ")
cpu_architecture=$(lscpu | grep "Architecture" | cut -d ":" -f2 | tr -d " ")
cache_line_length=$(grep "clflush size" /proc/cpuinfo | cut -d ":" -f2 | sort -u | tr -d " ")
l1_l2_l3_cache_size=$(lscpu | grep "L1d\|L1i\|L2\|L3")
total_system_ram=$(grep "MemTotal" /proc/meminfo | awk -F ":" '{print $2}' | awk '{$1=$1} END {print}')
number_of_gpus=$(nvidia-smi -q | grep "Attached GPUs" | cut -d ":" -f2 | awk '{$1=$1} END {print}')
gpu_model=$(nvidia-smi -q | grep "Product Name" | cut -d ":" -f2 | awk '{$1=$1} END {print}')
gpu_total_ram=$(nvidia-smi -q | grep "Total" | head -1 | cut -d ":" -f2 | awk '{$1=$1} END {print}')
filesystem_data=$(df /data | awk 'NR==2 {print $1}')
filesystem_datainbackup=$(df /datainbackup | awk 'NR==2 {print $1}')
total_size_data=$(df -h /data --output="size" | tail -n 1 | tr -d " ")
total_size_datainbackup=$(df -h /datainbackup --output="size" | tail -n 1 | tr -d " ")
total_free_space_data=$(df -h /data --output="avail" | tail -n 1 | awk '{$1=$1} END {print}')
total_free_space_datainbackup=$(df -h /datainbackup --output="avail" | tail -n 1 | awk '{$1=$1} END {print}')
linux_kernel_version=$(cat /proc/version)
os_distro_version=$(lsb_release -a)
python_path=$(which python3)
python_version=$(python --version)

echo "The model and clock frequency of the CPU is: $cpu_model."
echo "The number of physical CPUs, i.e. sockets in use is $number_of_cpus."
echo "Each physical CPU has $number_of_cores number of cores."
echo "The number of threads on each core is $number_of_threads."
echo "The instruction set architecture of the cpu is $cpu_architecture."
echo "The cache line length is $cache_line_length."
echo "The l1,l2 and l3 cache are divided as such:"
echo $l1_l2_l3_cache_size
echo "The total system ram is $total_system_ram."
echo "The total number of gpus $number_of_gpus."
echo "The gpu model is $gpu_model."
echo "The total amount of ram on the GPUs is $gpu_total_ram."
echo "The filesystem of /data is $filesystem_data and the filesystem of /datainbackup is $filesystem_datainbackup."
echo "The total amount of diskspace in /data is $total_size_data and the amount of free space is $total_free_space_data."
echo "The total amount of diskspace in /datainbackup is $total_size_datainbackup and the amount of free space is $total_free_space_datainbackup."
echo "The linux kernel version is $linux_kernel_version."
echo "The OS distro name and version is:" 
echo $os_distro_version
echo "The path to the python executable is $python_path and the python version is $python_version."
